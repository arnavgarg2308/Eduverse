function LanguageSelector({
  selectedLanguage = 'English',
  onLanguageChange,
}) {
  const languages = [
    {
      name: 'English',
      nativeName: 'English',
      code: 'EN',
    },
    {
      name: 'Hindi',
      nativeName: 'हिन्दी',
      code: 'HI',
    },
    {
      name: 'Bengali',
      nativeName: 'বাংলা',
      code: 'BN',
    },
    {
      name: 'Tamil',
      nativeName: 'தமிழ்',
      code: 'TA',
    },
    {
      name: 'Telugu',
      nativeName: 'తెలుగు',
      code: 'TE',
    },
    {
      name: 'Marathi',
      nativeName: 'मराठी',
      code: 'MR',
    },
  ]

  const currentLanguage =
    languages.find(
      (language) =>
        language.name === selectedLanguage,
    ) || {
      name: selectedLanguage,
      nativeName: selectedLanguage,
      code: '--',
    }

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
      {/* =====================================================
          HEADER
      ====================================================== */}
      <div className="flex items-start gap-3">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-orange-50 text-orange-600">
          🌐
        </div>

        <div className="min-w-0">
          <h3 className="font-black text-slate-900">
            Learning Language
          </h3>

          <p className="mt-1 text-xs leading-5 text-slate-500">
            Choose the language you want to learn in.
          </p>
        </div>
      </div>

      {/* =====================================================
          CURRENT LANGUAGE
      ====================================================== */}
      <div className="mt-5 rounded-2xl border border-orange-200 bg-gradient-to-r from-orange-50 to-amber-50 p-4">
        <div className="flex items-center justify-between gap-4">
          <div className="min-w-0">
            <p className="text-[10px] font-bold uppercase tracking-wider text-orange-500">
              Currently Learning In
            </p>

            <p className="mt-2 truncate font-black text-slate-900">
              {currentLanguage.nativeName}
            </p>

            <p className="mt-0.5 text-xs text-slate-500">
              {currentLanguage.name}
            </p>
          </div>

          <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white text-xs font-black text-orange-600 shadow-sm">
            {currentLanguage.code}
          </span>
        </div>
      </div>

      {/* =====================================================
          LANGUAGES
      ====================================================== */}
      <div className="mt-5">
        <div className="mb-3 flex items-center justify-between">
          <p className="text-xs font-bold text-slate-500">
            Available Languages
          </p>

          <span className="text-[10px] font-semibold text-slate-400">
            {languages.length} options
          </span>
        </div>

        <div className="grid grid-cols-2 gap-2">
          {languages.map((language) => {
            const isSelected =
              language.name === selectedLanguage

            return (
              <button
                key={language.code}
                type="button"
                onClick={() =>
                  onLanguageChange?.(
                    language.name,
                  )
                }
                aria-pressed={isSelected}
                className={`group rounded-xl border p-3 text-left transition-all duration-200 ${
                  isSelected
                    ? 'border-orange-300 bg-orange-50 shadow-sm'
                    : 'border-slate-100 bg-slate-50 hover:border-orange-200 hover:bg-orange-50/60'
                }`}
              >
                <div className="flex items-center justify-between gap-2">
                  <span
                    className={`text-sm font-bold ${
                      isSelected
                        ? 'text-orange-600'
                        : 'text-slate-800 group-hover:text-orange-600'
                    }`}
                  >
                    {language.nativeName}
                  </span>

                  {isSelected ? (
                    <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-orange-500 text-[10px] font-black text-white">
                      ✓
                    </span>
                  ) : (
                    <span className="text-[9px] font-bold text-slate-400">
                      {language.code}
                    </span>
                  )}
                </div>

                <p
                  className={`mt-1 text-[10px] ${
                    isSelected
                      ? 'text-orange-500'
                      : 'text-slate-400'
                  }`}
                >
                  {language.name}
                </p>
              </button>
            )
          })}
        </div>
      </div>

      {/* =====================================================
          AI TRANSLATION NOTE
      ====================================================== */}
      <div className="mt-5 rounded-2xl border border-slate-100 bg-slate-50 p-3.5">
        <div className="flex gap-3">
          <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-orange-50 text-sm text-orange-500">
            ✦
          </span>

          <div>
            <p className="text-xs font-bold text-slate-700">
              AI Language Adaptation
            </p>

            <p className="mt-1 text-[11px] leading-5 text-slate-500">
              Content will be adapted to your selected language while
              preserving the original meaning.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default LanguageSelector