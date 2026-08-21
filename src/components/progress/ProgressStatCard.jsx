function ProgressStatCard({
  icon,
  label,
  value,
  description,
  accent = 'orange',
}) {
  const accentStyles = {
    orange: {
      icon: 'bg-orange-50 text-orange-600',
      value: 'text-orange-600',
    },
    purple: {
      icon: 'bg-purple-50 text-purple-600',
      value: 'text-purple-600',
    },
    blue: {
      icon: 'bg-blue-50 text-blue-600',
      value: 'text-blue-600',
    },
    green: {
      icon: 'bg-emerald-50 text-emerald-600',
      value: 'text-emerald-600',
    },
  }

  const styles =
    accentStyles[accent] || accentStyles.orange

  return (
    <div className="group rounded-3xl border border-slate-200 bg-white p-5 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:border-orange-200 hover:shadow-lg">
      <div className="flex items-start justify-between gap-4">
        <div
          className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl text-lg transition-transform duration-300 group-hover:scale-105 ${styles.icon}`}
          aria-hidden="true"
        >
          {icon}
        </div>

        <span
          className={`text-2xl font-black ${styles.value}`}
        >
          {value}
        </span>
      </div>

      <h3 className="mt-5 text-sm font-black text-slate-900">
        {label}
      </h3>

      <p className="mt-1 text-xs leading-5 text-slate-500">
        {description}
      </p>
    </div>
  )
}

export default ProgressStatCard