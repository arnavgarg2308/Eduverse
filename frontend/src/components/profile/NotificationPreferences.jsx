function NotificationPreferences({
  preferences,
  onToggle,
}) {
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-start gap-3">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-orange-50 text-orange-600">
          🔔
        </div>

        <div>
          <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
            Stay Updated
          </p>

          <h2 className="mt-1 text-xl font-black text-slate-900">
            Notifications
          </h2>

          <p className="mt-1 text-sm leading-6 text-slate-500">
            Choose which updates you would like to receive.
          </p>
        </div>
      </div>

      <div className="mt-6 space-y-3">
        {preferences.map((preference) => (
          <NotificationItem
            key={preference.id}
            preference={preference}
            onToggle={onToggle}
          />
        ))}
      </div>

      <div className="mt-5 rounded-2xl bg-slate-50 p-4">
        <p className="text-xs font-semibold text-slate-600">
          💡 Tip
        </p>

        <p className="mt-1 text-xs leading-5 text-slate-500">
          Keep learning reminders enabled to maintain a consistent
          study routine.
        </p>
      </div>
    </section>
  )
}

function NotificationItem({
  preference,
  onToggle,
}) {
  return (
    <button
      type="button"
      onClick={() => onToggle(preference.id)}
      className={`flex w-full items-center gap-4 rounded-2xl border p-4 text-left transition-all ${
        preference.enabled
          ? 'border-orange-100 bg-orange-50/60'
          : 'border-slate-100 bg-slate-50 hover:border-slate-200 hover:bg-white'
      }`}
    >
      <div className="min-w-0 flex-1">
        <h3 className="text-sm font-bold text-slate-800">
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

export default NotificationPreferences