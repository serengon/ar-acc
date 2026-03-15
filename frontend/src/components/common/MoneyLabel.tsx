import styles from "./MoneyLabel.module.css";

interface MoneyLabelProps {
  value: number;
  className?: string;
}

export function MoneyLabel({ value, className }: MoneyLabelProps) {
  const formatted = value.toLocaleString("es-AR", {
    style: "currency",
    currency: "ARS",
  });

  return <span className={`${styles.money} ${className ?? ""}`}>{formatted}</span>;
}
