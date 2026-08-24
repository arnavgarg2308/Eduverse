function Badge({
  children,
  variant = 'default',
  className = '',
}) {
  const variants = {
    default: 'bg-slate-100 text-slate-700',
    primary: 'bg-orange-100 text-orange-700',
    success: 'bg-green-100 text-green-700',
    warning: 'bg-amber-100 text-amber-700',
    danger: 'bg-red-100 text-red-700',
    info: 'bg-cyan-100 text-cyan-700',
  }

  const selectedVariant =
    variants[variant] || variants.default

  return (
    <span
      className={[
        'inline-flex items-center rounded-full',
        'px-2.5 py-1 text-xs font-bold',
        'whitespace-nowrap',
        selectedVariant,
        className,
      ]
        .filter(Boolean)
        .join(' ')}
    >
      {children}
    </span>
  )
}

export default Badge