function AccessibilityPreferences({
  preferences,
  onToggle,
}) {
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div>
        <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
          Inclusive Learning
        </p>

        <h2 className="mt-1 text-xl font-black text-slate-900">
          Accessibility
        </h2>

        <p className="mt-1 text-sm leading-6 text-slate-500">
          Adjust EduMorph to make learning more comfortable and
          accessible for you.
        </p>
      </div>

      <div className="mt-6 space-y-3">
        {preferences.map((preference) => (
          <AccessibilityItem
            key={preference.id}
            preference={preference}
            onToggle={onToggle}
          />
        ))}
      </div>

      <div className="mt-5 rounded-2xl border border-orange-100 bg-orange-50 p-4">
        <div className="flex gap-3">
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-white text-orange-600 shadow-sm">
            ♿
          </div>

          <div>
            <p className="text-xs font-bold text-orange-700">
              Designed for every learner
            </p>

            <p className="mt-1 text-xs leading-5 text-orange-700/70">
              These settings can be used throughout your learning
              experience to make educational content easier to access.
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}

function AccessibilityItem({
  preference,
  onToggle,
}) {
  return (
    <button
      type="button"
      onClick={() => onToggle(preference.id)}
      className={`flex w-full items-center gap-4 rounded-2xl border p-4 text-left transition-all ${
        preference.enabled
          ? 'border-orange-200 bg-orange-50'
          : 'border-slate-100 bg-slate-50 hover:border-slate-200 hover:bg-white'
      }`}
    >
      <div
        className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-xl text-xs font-bold ${
          preference.enabled
            ? 'bg-orange-500 text-white'
            : 'bg-white text-slate-500'
        }`}
      >
        {preference.icon}
      </div>

      <div className="min-w-0 flex-1">
        <h3
          className={`text-sm font-bold ${
            preference.enabled
              ? 'text-orange-700'
              : 'text-slate-800'
          }`}
        >
          {preference.title}
        </h3>

        <p className="mt-1 text-xs leading-5 text-slate-500">
          {preference.description}
        </p>
      </div>

      <div
        className={`relative h-6 w-10 shrink-0 rounded-full transition-colors ${
          preference.enabled
            ? 'bg-orange-500'
            : 'bg-slate-300'
        }`}
      >
        <span
          className={`absolute top-1 h-4 w-4 rounded-full bg-white shadow-sm transition-transform ${
            preference.enabled
              ? 'translate-x-5'
              : 'translate-x-1'
          }`}
        />
      </div>
    </button>
  )
}

export default AccessibilityPreferences