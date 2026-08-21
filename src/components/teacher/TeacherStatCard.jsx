function TeacherStatCard({
  icon,
  label,
  value,
  description,
  accent = 'orange',
}) {
  const accentStyles = {
    orange: 'bg-orange-50 text-orange-600',
    blue: 'bg-blue-50 text-blue-600',
    purple: 'bg-purple-50 text-purple-600',
    green: 'bg-emerald-50 text-emerald-600',
  }

  return (
    <div className="group rounded-3xl border border-slate-200 bg-white p-5 shadow-sm transition duration-300 hover:-translate-y-1 hover:border-orange-200 hover:shadow-lg">
      <div className="flex items-start justify-between">
        <div
          className={`flex h-11 w-11 items-center justify-center rounded-2xl text-lg ${
            accentStyles[accent] || accentStyles.orange
          }`}
        >
          {icon}
        </div>

        <span className="text-2xl font-black text-slate-900">
          {value}
        </span>
      </div>

      <h3 className="mt-5 text-sm font-bold text-slate-900">
        {label}
      </h3>

      <p className="mt-1 text-xs leading-5 text-slate-500">
        {description}
      </p>
    </div>
  )
}

export default TeacherStatCard
