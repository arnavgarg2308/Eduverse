function LearningPreferences({
  preferences,
  languages,
  modes,
  onLanguageChange,
  onModeChange,
}) {
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div>
        <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
          Personalization
        </p>

        <h2 className="mt-1 text-xl font-black text-slate-900">
          Learning Preferences
        </h2>

        <p className="mt-1 text-sm leading-6 text-slate-500">
          Customize how EduMorph presents your learning content.
        </p>
      </div>

      {/* Language */}
      <div className="mt-6">
        <label className="text-sm font-bold text-slate-800">
          Preferred Language
        </label>

        <p className="mt-1 text-xs text-slate-500">
          Choose the language used for your learning experience.
        </p>

        <div className="mt-3 grid gap-2 sm:grid-cols-3">
          {languages.map((language) => {
            const selected =
              preferences.language === language.name

            return (
              <button
                key={language.code}
                type="button"
                onClick={() =>
                  onLanguageChange(language.name)
                }
                className={`rounded-2xl border p-4 text-left transition ${
                  selected
                    ? 'border-orange-300 bg-orange-50 shadow-sm'
                    : 'border-slate-100 bg-slate-50 hover:border-orange-200 hover:bg-orange-50/50'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span
                    className={`font-bold ${
                      selected
                        ? 'text-orange-600'
                        : 'text-slate-800'
                    }`}
                  >
                    {language.nativeName}
                  </span>

                  {selected && (
                    <span className="flex h-5 w-5 items-center justify-center rounded-full bg-orange-500 text-[10px] text-white">
                      ✓
                    </span>
                  )}
                </div>

                <p className="mt-1 text-xs text-slate-400">
                  {language.name}
                </p>
              </button>
            )
          })}
        </div>
      </div>

      {/* Learning Mode */}
      <div className="mt-7 border-t border-slate-100 pt-6">
        <label className="text-sm font-bold text-slate-800">
          Preferred Learning Mode
        </label>

        <p className="mt-1 text-xs text-slate-500">
          Choose the format that works best for you.
        </p>

        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          {modes.map((mode) => {
            const selected =
              preferences.learningMode === mode.label

            return (
              <button
                key={mode.id}
                type="button"
                onClick={() => onModeChange(mode.label)}
                className={`flex items-start gap-3 rounded-2xl border p-4 text-left transition ${
                  selected
                    ? 'border-orange-300 bg-orange-50'
                    : 'border-slate-100 bg-slate-50 hover:border-orange-200 hover:bg-white'
                }`}
              >
                <div
                  className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl text-sm font-bold ${
                    selected
                      ? 'bg-orange-500 text-white'
                      : 'bg-white text-slate-500'
                  }`}
                >
                  {mode.icon}
                </div>

                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="text-sm font-bold text-slate-900">
                      {mode.label}
                    </h3>

                    {selected && (
                      <span className="text-xs font-bold text-orange-500">
                        ✓
                      </span>
                    )}
                  </div>

                  <p className="mt-1 text-xs leading-5 text-slate-500">
                    {mode.description}
                  </p>
                </div>
              </button>
            )
          })}
        </div>
      </div>

      {/* Difficulty */}
      <div className="mt-7 border-t border-slate-100 pt-6">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <label className="text-sm font-bold text-slate-800">
              Content Difficulty
            </label>

            <p className="mt-1 text-xs text-slate-500">
              EduMorph adjusts difficulty based on your performance.
            </p>
          </div>

          <span className="rounded-xl bg-orange-50 px-4 py-2 text-xs font-bold text-orange-600">
            {preferences.contentDifficulty}
          </span>
        </div>
      </div>
    </section>
  )
}

export default LearningPreferences