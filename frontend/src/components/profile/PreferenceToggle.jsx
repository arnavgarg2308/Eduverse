function PreferenceToggle({
  icon,
  title,
  description,
  enabled,
  onChange,
}) {
  return (
    <button
      type="button"
      onClick={() => onChange(!enabled)}
      className={`flex w-full items-center gap-4 rounded-2xl border p-4 text-left transition-all ${
        enabled
          ? 'border-orange-200 bg-orange-50'
          : 'border-slate-100 bg-slate-50 hover:border-slate-200 hover:bg-white'
      }`}
    >
      <div
        className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-xl text-sm font-bold ${
          enabled
            ? 'bg-orange-500 text-white'
            : 'bg-white text-slate-500'
        }`}
      >
        {icon}
      </div>

      <div className="min-w-0 flex-1">
        <h3
          className={`text-sm font-bold ${
            enabled
              ? 'text-orange-700'
              : 'text-slate-800'
          }`}
        >
          {title}
        </h3>

        <p className="mt-1 text-xs leading-5 text-slate-500">
          {description}
        </p>
      </div>

      <div
        className={`relative h-6 w-10 shrink-0 rounded-full transition-colors ${
          enabled
            ? 'bg-orange-500'
            : 'bg-slate-300'
        }`}
      >
        <span
          className={`absolute top-1 h-4 w-4 rounded-full bg-white shadow-sm transition-transform ${
            enabled
              ? 'translate-x-5'
              : 'translate-x-1'
          }`}
        />
      </div>
    </button>
  )
}

export default PreferenceToggle