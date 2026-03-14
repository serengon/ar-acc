import type { ButtonHTMLAttributes, ReactNode } from "react";

import { Spinner } from "@/components/common/Spinner";

import styles from "./Button.module.css";

type ButtonVariant = "primary" | "secondary" | "ghost" | "danger" | "system";
type ButtonSize = "sm" | "md" | "lg";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  icon?: ReactNode;
  iconRight?: ReactNode;
  loading?: boolean;
  children?: ReactNode;
}

const spinnerSizeMap: Record<ButtonSize, "sm" | "md" | "lg"> = {
  sm: "sm",
  md: "sm",
  lg: "md",
};

export function Button({
  variant = "secondary",
  size = "md",
  icon,
  iconRight,
  loading = false,
  children,
  className,
  disabled,
  ...rest
}: ButtonProps) {
  const isIconOnly = !children && (!!icon || !!iconRight);

  const classNames = [
    styles.button,
    styles[variant],
    styles[size],
    isIconOnly ? styles.iconOnly : "",
    className ?? "",
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <button
      className={classNames}
      disabled={disabled || loading}
      {...rest}
    >
      {loading ? (
        <Spinner size={spinnerSizeMap[size]} />
      ) : (
        <>
          {icon && <span className={styles.icon}>{icon}</span>}
          {children}
          {iconRight && <span className={styles.icon}>{iconRight}</span>}
        </>
      )}
    </button>
  );
}
