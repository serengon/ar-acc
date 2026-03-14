import styles from "./MoneyLabel.module.css";

interface MoneyLabelProps {
  value: number;
  className?: string;
}

export function MoneyLabel({ value, className }: MoneyLabelProps) {
  const formatted = value.toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  });

  return <span className={`${styles.money} ${className ?? ""}`}>{formatted}</span>;
}
