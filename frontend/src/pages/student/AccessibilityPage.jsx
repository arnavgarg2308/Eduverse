import { useState } from 'react'
import DashboardLayout from '../../components/layout/DashboardLayout'

const accessibilityOptions = [
  {
    id: 'large-text',
    title: 'Larger Text',
    description:
      'Increase text size across the learning interface for easier reading.',
    icon: 'Aa',
  },
  {
    id: 'high-contrast',
    title: 'High Contrast',
    description:
      'Improve the contrast between text, backgrounds and interface elements.',
    icon: '◐',
  },
  {
    id: 'reduced-motion',
    title: 'Reduce Motion',
    description:
      'Minimize animations and transitions throughout EduVerse.',
    icon: '≋',
  },
  {
    id: 'focus-mode',
    title: 'Focus Mode',
    description:
      'Reduce visual distractions and keep your attention on the current lesson.',
    icon: '◎',
  },
]

const learningModes = [
  {
    id: 'visual',
    title: 'Visual Learning',
    description:
      'Prefer diagrams, illustrations and visual explanations.',
    icon: '◈',
  },
  {
    id: 'audio',
    title: 'Audio Learning',
    description:
      'Use narration and audio explanations when available.',
    icon: '♫',
  },
  {
    id: 'simplified',
    title: 'Simplified Content',
    description:
      'Prefer shorter explanations with simpler language.',
    icon: '≡',
  },
]

function AccessibilityPage() {
  const [settings, setSettings] = useState({
    'large-text': false,
    'high-contrast': false,
    'reduced-motion': false,
    'focus-mode': false,
  })

  const [selectedMode, setSelectedMode] =
    useState('visual')

  const [saved, setSaved] = useState(false)

  const toggleSetting = (id) => {
    setSettings((current) => ({
      ...current,
      [id]: !current[id],
    }))

    setSaved(false)
  }

  const handleSave = () => {
    setSaved(true)

    setTimeout(() => {
      setSaved(false)
    }, 2500)
  }

  return (
    <DashboardLayout
      role="student"
      title="Accessibility"
    >
      <div className="mx-auto max-w-6xl">
        {/* =================================================
            INTRO
        ================================================== */}
        <section>
          <p className="text-sm font-bold uppercase tracking-[0.15em] text-orange-500">
            Personalize Your Experience
          </p>

          <h2 className="mt-2 text-3xl font-black tracking-tight text-slate-900 sm:text-4xl">
            Learning that works for you.
          </h2>

          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500 sm:text-base">
            Customize EduVerse so your learning experience feels
            comfortable, focused and accessible.
          </p>
        </section>

        {/* =================================================
            ACCESSIBILITY SETTINGS
        ================================================== */}
        <section className="mt-8">
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
                Display & Accessibility
              </p>

              <h3 className="mt-1 text-xl font-black text-slate-900">
                Interface Preferences
              </h3>

              <p className="mt-1 text-sm text-slate-500">
                Choose the settings that make EduVerse easier for you
                to use.
              </p>
            </div>

            <div className="mt-6 grid gap-4 md:grid-cols-2">
              {accessibilityOptions.map((option) => (
                <SettingCard
                  key={option.id}
                  option={option}
                  enabled={settings[option.id]}
                  onToggle={() =>
                    toggleSetting(option.id)
                  }
                />
              ))}
            </div>
          </div>
        </section>

        {/* =================================================
            LEARNING MODE
        ================================================== */}
        <section className="mt-6">
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
                Learning Preferences
              </p>

              <h3 className="mt-1 text-xl font-black text-slate-900">
                Preferred Learning Mode
              </h3>

              <p className="mt-1 text-sm text-slate-500">
                Tell EduVerse how you prefer educational content to
                be presented.
              </p>
            </div>

            <div className="mt-6 grid gap-4 md:grid-cols-3">
              {learningModes.map((mode) => {
                const selected =
                  selectedMode === mode.id

                return (
                  <button
                    key={mode.id}
                    type="button"
                    onClick={() => {
                      setSelectedMode(mode.id)
                      setSaved(false)
                    }}
                    className={`rounded-2xl border p-5 text-left transition ${
                      selected
                        ? 'border-orange-300 bg-orange-50 shadow-sm'
                        : 'border-slate-200 bg-white hover:border-orange-200 hover:bg-orange-50/50'
                    }`}
                  >
                    <div
                      className={`flex h-11 w-11 items-center justify-center rounded-xl text-lg font-bold ${
                        selected
                          ? 'bg-orange-500 text-white'
                          : 'bg-slate-100 text-slate-500'
                      }`}
                    >
                      {mode.icon}
                    </div>

                    <div className="mt-4 flex items-center justify-between gap-3">
                      <h4 className="text-sm font-black text-slate-900">
                        {mode.title}
                      </h4>

                      {selected && (
                        <span className="text-xs font-black text-orange-600">
                          ✓
                        </span>
                      )}
                    </div>

                    <p className="mt-2 text-xs leading-5 text-slate-500">
                      {mode.description}
                    </p>
                  </button>
                )
              })}
            </div>
          </div>
        </section>

        {/* =================================================
            LANGUAGE
        ================================================== */}
        <section className="mt-6">
          <div className="rounded-3xl border border-orange-100 bg-gradient-to-r from-orange-50 to-amber-50 p-6">
            <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
                  Language
                </p>

                <h3 className="mt-1 text-xl font-black text-slate-900">
                  Prefer learning in your language?
                </h3>

                <p className="mt-1 max-w-xl text-sm leading-6 text-slate-500">
                  Regional and multilingual learning options will be
                  connected to the EduVerse AI translation system.
                </p>
              </div>

              <div className="shrink-0 rounded-2xl border border-orange-200 bg-white px-5 py-4">
                <p className="text-[10px] font-bold uppercase tracking-wider text-orange-500">
                  Current Language
                </p>

                <p className="mt-1 text-sm font-black text-slate-900">
                  English
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* =================================================
            SAVE
        ================================================== */}
        <section className="mt-6 pb-8">
          <div className="flex flex-col gap-4 rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:flex-row sm:items-center sm:justify-between">
            <div>
              {saved ? (
                <p className="text-sm font-bold text-emerald-600">
                  ✓ Accessibility preferences saved.
                </p>
              ) : (
                <p className="text-sm text-slate-500">
                  Your preferences will be applied to future learning
                  sessions.
                </p>
              )}
            </div>

            <button
              type="button"
              onClick={handleSave}
              className="rounded-xl bg-orange-500 px-6 py-3 text-sm font-bold text-white transition hover:bg-orange-600"
            >
              Save Preferences
            </button>
          </div>
        </section>
      </div>
    </DashboardLayout>
  )
}

function SettingCard({
  option,
  enabled,
  onToggle,
}) {
  return (
    <div
      className={`rounded-2xl border p-5 transition ${
        enabled
          ? 'border-orange-200 bg-orange-50/60'
          : 'border-slate-200 bg-white'
      }`}
    >
      <div className="flex items-start justify-between gap-4">
        <div
          className={`flex h-11 w-11 items-center justify-center rounded-xl text-sm font-black ${
            enabled
              ? 'bg-orange-500 text-white'
              : 'bg-slate-100 text-slate-500'
          }`}
        >
          {option.icon}
        </div>

        <button
          type="button"
          onClick={onToggle}
          aria-label={`Toggle ${option.title}`}
          className={`relative h-7 w-12 shrink-0 rounded-full transition ${
            enabled
              ? 'bg-orange-500'
              : 'bg-slate-300'
          }`}
        >
          <span
            className={`absolute top-1 h-5 w-5 rounded-full bg-white shadow-sm transition ${
              enabled
                ? 'left-6'
                : 'left-1'
            }`}
          />
        </button>
      </div>

      <h4 className="mt-4 text-sm font-black text-slate-900">
        {option.title}
      </h4>

      <p className="mt-2 text-xs leading-5 text-slate-500">
        {option.description}
      </p>

      <p
        className={`mt-4 text-[10px] font-bold uppercase tracking-wider ${
          enabled
            ? 'text-orange-600'
            : 'text-slate-400'
        }`}
      >
        {enabled ? 'Enabled' : 'Disabled'}
      </p>
    </div>
  )
}

export default AccessibilityPage