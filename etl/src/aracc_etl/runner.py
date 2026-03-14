import logging
import os

import click
from neo4j import GraphDatabase

from aracc_etl.linking_hooks import run_post_load_hooks
from aracc_etl.pipelines.afip_contribuyentes import AfipContribuyentesPipeline
from aracc_etl.pipelines.agn import AgnPipeline
from aracc_etl.pipelines.bcra_deudores import BcraDeudoresPipeline
from aracc_etl.pipelines.boletin_oficial import BoletinOficialPipeline
from aracc_etl.pipelines.cij_judicial import CijJudicialPipeline
from aracc_etl.pipelines.cne_elecciones import CneEleccionesPipeline
from aracc_etl.pipelines.cnv import CnvPipeline
from aracc_etl.pipelines.comprar import ComprarPipeline
from aracc_etl.pipelines.ddjj_funcionarios import DdjjFuncionariosPipeline
from aracc_etl.pipelines.educacion import EducacionPipeline
from aracc_etl.pipelines.eu_sanctions import EuSanctionsPipeline
from aracc_etl.pipelines.hcdn_gastos import HcdnGastosPipeline
from aracc_etl.pipelines.hsn_gastos import HsnGastosPipeline
from aracc_etl.pipelines.icij import ICIJPipeline
from aracc_etl.pipelines.igj_sociedades import IgjSociedadesPipeline
from aracc_etl.pipelines.oa_sanciones import OaSancionesPipeline
from aracc_etl.pipelines.ofac import OfacPipeline
from aracc_etl.pipelines.opensanctions import OpenSanctionsPipeline
from aracc_etl.pipelines.presupuesto_abierto import PresupuestoAbiertoPipeline
from aracc_etl.pipelines.sipa_empleo import SipaEmpleoPipeline
from aracc_etl.pipelines.sisa_salud import SisaSaludPipeline
from aracc_etl.pipelines.uif_peps import UifPepsPipeline
from aracc_etl.pipelines.un_sanctions import UnSanctionsPipeline
from aracc_etl.pipelines.world_bank import WorldBankPipeline

PIPELINES: dict[str, type] = {
    # ── Tier 0: Core identity & procurement ──
    "afip_contribuyentes": AfipContribuyentesPipeline,
    "igj_sociedades": IgjSociedadesPipeline,
    "comprar": ComprarPipeline,
    "cne_elecciones": CneEleccionesPipeline,
    "boletin_oficial": BoletinOficialPipeline,
    # ── Tier 1: High-value enrichment ──
    "bcra_deudores": BcraDeudoresPipeline,
    "cnv": CnvPipeline,
    "agn": AgnPipeline,
    "hcdn_gastos": HcdnGastosPipeline,
    "hsn_gastos": HsnGastosPipeline,
    "oa_sanciones": OaSancionesPipeline,
    "ddjj_funcionarios": DdjjFuncionariosPipeline,
    "uif_peps": UifPepsPipeline,
    "presupuesto_abierto": PresupuestoAbiertoPipeline,
    "sipa_empleo": SipaEmpleoPipeline,
    "sisa_salud": SisaSaludPipeline,
    "educacion": EducacionPipeline,
    "cij_judicial": CijJudicialPipeline,
    # ── International (shared with br/acc) ──
    "icij": ICIJPipeline,
    "opensanctions": OpenSanctionsPipeline,
    "ofac": OfacPipeline,
    "eu_sanctions": EuSanctionsPipeline,
    "un_sanctions": UnSanctionsPipeline,
    "world_bank": WorldBankPipeline,
}


@click.group()
def cli() -> None:
    """AR-ACC ETL — Data ingestion pipelines for Argentine public data."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


@cli.command()
@click.option("--source", required=True, help="Pipeline name (see 'sources' command)")
@click.option("--neo4j-uri", default="bolt://localhost:7687", help="Neo4j URI")
@click.option("--neo4j-user", default="neo4j", help="Neo4j user")
@click.option("--neo4j-password", required=True, help="Neo4j password")
@click.option("--neo4j-database", default="neo4j", help="Neo4j database")
@click.option("--data-dir", default="./data", help="Directory for downloaded data")
@click.option("--limit", type=int, default=None, help="Limit rows processed")
@click.option("--chunk-size", type=int, default=50_000, help="Chunk size for batch processing")
@click.option(
    "--linking-tier",
    type=click.Choice(["community", "full"]),
    default=os.getenv("LINKING_TIER", "full"),
    show_default=True,
    help="Post-load linking strategy tier",
)
@click.option("--streaming/--no-streaming", default=False, help="Streaming mode")
@click.option("--start-phase", type=int, default=1, help="Skip to phase N")
@click.option("--history/--no-history", default=False, help="Enable history mode when supported")
def run(
    source: str,
    neo4j_uri: str,
    neo4j_user: str,
    neo4j_password: str,
    neo4j_database: str,
    data_dir: str,
    limit: int | None,
    chunk_size: int,
    linking_tier: str,
    streaming: bool,
    start_phase: int,
    history: bool,
) -> None:
    """Run an ETL pipeline."""
    os.environ["NEO4J_DATABASE"] = neo4j_database

    if source not in PIPELINES:
        available = ", ".join(PIPELINES.keys())
        raise click.ClickException(f"Unknown source: {source}. Available: {available}")

    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
    try:
        pipeline_cls = PIPELINES[source]
        pipeline = pipeline_cls(
            driver=driver,
            data_dir=data_dir,
            limit=limit,
            chunk_size=chunk_size,
            history=history,
        )

        if streaming and hasattr(pipeline, "run_streaming"):
            pipeline.run_streaming(start_phase=start_phase)
        else:
            pipeline.run()

        run_post_load_hooks(
            driver=driver,
            source=source,
            neo4j_database=neo4j_database,
            linking_tier=linking_tier,
        )
    finally:
        driver.close()


@cli.command()
@click.option("--status", "show_status", is_flag=True, help="Show ingestion status from Neo4j")
@click.option("--neo4j-uri", default="bolt://localhost:7687", help="Neo4j URI")
@click.option("--neo4j-user", default="neo4j")
@click.option("--neo4j-password", default=None)
def sources(show_status: bool, neo4j_uri: str, neo4j_user: str, neo4j_password: str | None) -> None:
    """List available data sources."""
    if not show_status:
        click.echo("Available pipelines:")
        for name in sorted(PIPELINES):
            click.echo(f"  {name}")
        return

    if not neo4j_password:
        neo4j_password = os.environ.get("NEO4J_PASSWORD", "")
    if not neo4j_password:
        raise click.ClickException(
            "--neo4j-password or NEO4J_PASSWORD env var required for --status"
        )

    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
    try:
        with driver.session() as session:
            result = session.run(
                "MATCH (r:IngestionRun) "
                "WITH r ORDER BY r.started_at DESC "
                "WITH r.source_id AS sid, collect(r)[0] AS latest "
                "RETURN latest ORDER BY sid"
            )
            runs = {r["latest"]["source_id"]: dict(r["latest"]) for r in result}

        click.echo(
            f"{'Source':<25} {'Status':<15} {'Rows In':>10} {'Loaded':>10} "
            f"{'Started':<20} {'Finished':<20}"
        )
        click.echo("-" * 105)

        for name in sorted(PIPELINES):
            run = runs.get(name, {})
            click.echo(
                f"{name:<25} "
                f"{run.get('status', '-'):<15} "
                f"{run.get('rows_in', 0):>10,} "
                f"{run.get('rows_loaded', 0):>10,} "
                f"{str(run.get('started_at', '-')):<20} "
                f"{str(run.get('finished_at', '-')):<20}"
            )
    finally:
        driver.close()


if __name__ == "__main__":
    cli()
