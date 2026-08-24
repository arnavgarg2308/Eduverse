function ProgressBar({
  value = 0,
  label,
  showPercentage = true,
  size = 'md',
  className = '',
}) {
  const safeValue = Math.min(Math.max(value, 0), 100)

  const sizes = {
    sm: 'h-1.5',
    md: 'h-2.5',
    lg: 'h-4',
  }

  return (
    <div className={`w-full ${className}`}>
      {(label || showPercentage) && (
        <div className="mb-2 flex items-center justify-between">
          {label && (
            <span className="text-sm font-medium text-slate-700">
              {label}
            </span>
          )}

          {showPercentage && (
            <span className="text-sm font-semibold text-slate-600">
              {safeValue}%
            </span>
          )}
        </div>
      )}

      <div
        className={`w-full overflow-hidden rounded-full bg-slate-200 ${sizes[size]}`}
        role="progressbar"
        aria-valuenow={safeValue}
        aria-valuemin="0"
        aria-valuemax="100"
      >
        <div
          className={`h-full rounded-full bg-blue-600 transition-all duration-500 ${sizes[size]}`}
          style={{ width: `${safeValue}%` }}
        />
      </div>
    </div>
  )
}

export default ProgressBar