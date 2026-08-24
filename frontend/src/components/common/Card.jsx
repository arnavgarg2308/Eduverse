function Card({
  children,
  className = '',
  padding = 'md',
  hover = false,
}) {
  const paddingStyles = {
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  }

  const selectedPadding =
    paddingStyles[padding] || paddingStyles.md

  return (
    <div
      className={[
        'rounded-2xl border border-slate-200',
        'bg-white shadow-sm',
        'transition-colors duration-200',
        selectedPadding,
        hover
          ? 'transition-all duration-200 hover:-translate-y-1 hover:border-orange-200 hover:shadow-md'
          : '',
        className,
      ]
        .filter(Boolean)
        .join(' ')}
    >
      {children}
    </div>
  )
}

export default Card