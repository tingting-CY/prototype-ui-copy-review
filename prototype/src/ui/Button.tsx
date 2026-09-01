import type { ButtonHTMLAttributes, ReactNode } from 'react'
import './button.css'

export type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'accent' | 'orb' | 'danger'
export type ButtonSize = 'sm' | 'md' | 'lg'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant
  size?: ButtonSize
  block?: boolean
  iconLeft?: ReactNode
  iconRight?: ReactNode
}

/**
 * Handhold primary action button.
 * Variants: primary (ink) · secondary · ghost · accent (violet) · orb (brand gradient) · danger.
 */
export function Button({
  variant = 'primary',
  size = 'md',
  block = false,
  iconLeft = null,
  iconRight = null,
  className = '',
  children,
  ...rest
}: ButtonProps) {
  const cls = [
    'hh-btn',
    `hh-btn--${variant}`,
    size !== 'md' ? `hh-btn--${size}` : '',
    block ? 'hh-btn--block' : '',
    className,
  ]
    .filter(Boolean)
    .join(' ')

  return (
    <button type="button" className={cls} {...rest}>
      {iconLeft}
      {children != null && <span>{children}</span>}
      {iconRight}
    </button>
  )
}
