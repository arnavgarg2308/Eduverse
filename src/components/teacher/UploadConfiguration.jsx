import PreferenceToggle from '../profile/PreferenceToggle'

function UploadConfiguration({
  category,
  difficulty,
  language,
  categories,
  difficultyLevels,
  languages,
  accessibilityOptions,
  onCategoryChange,
  onDifficultyChange,
  onLanguageChange,
  onAccessibilityToggle,
}) {
  return (
    <div className="space-y-6">
      {/* =====================================================
          BASIC INFORMATION
      ====================================================== */}
      <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
            Content Details
          </p>

          <h2 className="mt-1 text-xl font-black text-slate-900">
            Configure Your Content
          </h2>

          <p className="mt-1 text-sm leading-6 text-slate-500">
            Tell EduMorph a little about this learning material.
          </p>
        </div>

        <div className="mt-6 grid gap-5 md:grid-cols-3">
          {/* Category */}
          <SelectField
            label="Subject"
            value={category}
            options={categories}
            onChange={onCategoryChange}
          />

          {/* Difficulty */}
          <SelectField
            label="Difficulty"
            value={difficulty}
            options={difficultyLevels}
            onChange={onDifficultyChange}
          />

          {/* Language */}
          <div>
            <label className="text-sm font-bold text-slate-800">
              Output Language
            </label>

            <select
              value={language}
              onChange={(event) =>
                onLanguageChange(event.target.value)
              }
              className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm font-medium text-slate-700 outline-none transition focus:border-orange-400 focus:ring-2 focus:ring-orange-100"
            >
              {languages.map((item) => (
                <option
                  key={item.code}
                  value={item.name}
                >
                  {item.nativeName} — {item.name}
                </option>
              ))}
            </select>

            <p className="mt-2 text-[11px] text-slate-400">
              AI-generated learning content will use this language.
            </p>
          </div>
        </div>
      </section>

      {/* =====================================================
          AI FEATURES
      ====================================================== */}
      <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
            AI Transformation
          </p>

          <h2 className="mt-1 text-xl font-black text-slate-900">
            Choose Learning Outputs
          </h2>

          <p className="mt-1 text-sm leading-6 text-slate-500">
            Select the learning formats EduMorph should generate.
          </p>
        </div>

        <div className="mt-6 space-y-3">
          {accessibilityOptions.map((option) => (
            <PreferenceToggle
              key={option.id}
              icon={option.icon}
              title={option.title}
              description={option.description}
              enabled={option.enabled}
              onChange={() =>
                onAccessibilityToggle(option.id)
              }
            />
          ))}
        </div>
      </section>

      {/* =====================================================
          AI INFO
      ====================================================== */}
      <div className="rounded-3xl border border-orange-100 bg-gradient-to-r from-orange-50 to-amber-50 p-5">
        <div className="flex gap-4">
          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-white text-orange-600 shadow-sm">
            ✦
          </div>

          <div>
            <h3 className="text-sm font-black text-slate-900">
              EduMorph AI will do the rest
            </h3>

            <p className="mt-1 text-xs leading-5 text-slate-500">
              Your selected content will be analyzed and transformed
              into personalized learning resources based on these
              settings.
            </p>

            <div className="mt-3 flex flex-wrap gap-2">
              <InfoPill text="Content Analysis" />
              <InfoPill text="Multilingual" />
              <InfoPill text="Accessible" />
              <InfoPill text="AI Generated" />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function SelectField({
  label,
  value,
  options,
  onChange,
}) {
  return (
    <div>
      <label className="text-sm font-bold text-slate-800">
        {label}
      </label>

      <select
        value={value}
        onChange={(event) =>
          onChange(event.target.value)
        }
        className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm font-medium text-slate-700 outline-none transition focus:border-orange-400 focus:ring-2 focus:ring-orange-100"
      >
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </div>
  )
}

function InfoPill({ text }) {
  return (
    <span className="rounded-lg bg-white px-2.5 py-1.5 text-[10px] font-bold text-orange-600 shadow-sm">
      ✓ {text}
    </span>
  )
}

export default UploadConfiguration