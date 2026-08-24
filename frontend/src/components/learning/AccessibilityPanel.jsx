import { useState } from 'react'

function AccessibilityPanel() {
  const [dyslexiaMode, setDyslexiaMode] = useState(false)
  const [focusMode, setFocusMode] = useState(false)
  const [highContrast, setHighContrast] = useState(false)
  const [largerText, setLargerText] = useState(false)
  const [narration, setNarration] = useState(true)

  const activeSettings = [
    {
      label: 'Dyslexia Friendly',
      enabled: dyslexiaMode,
    },
    {
      label: 'Focus Mode',
      enabled: focusMode,
    },
    {
      label: 'High Contrast',
      enabled: highContrast,
    },
    {
      label: 'Larger Text',
      enabled: largerText,
    },
    {
      label: 'Narration',
      enabled: narration,
    },
  ]

  const activeCount = activeSettings.filter(
    (setting) => setting.enabled,
  ).length

  const resetSettings = () => {
    setDyslexiaMode(false)
    setFocusMode(false)
    setHighContrast(false)
    setLargerText(false)
    setNarration(false)
  }

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
      {/* =====================================================
          HEADER
      ====================================================== */}
      <div className="flex items-start gap-3">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-orange-50 text-orange-600">
          ♿
        </div>

        <div className="min-w-0">
          <h3 className="font-black text-slate-900">
            Accessibility
          </h3>

          <p className="mt-1 text-xs leading-5 text-slate-500">
            Customize your learning experience.
          </p>
        </div>
      </div>

      {/* =====================================================
          CONTROLS
      ====================================================== */}
      <div className="mt-5 space-y-2">
        <AccessibilityToggle
          icon="Aa"
          title="Dyslexia Friendly"
          description="Improve readability and spacing"
          enabled={dyslexiaMode}
          onChange={setDyslexiaMode}
        />

        <AccessibilityToggle
          icon="◎"
          title="Focus Mode"
          description="Reduce visual distractions"
          enabled={focusMode}
          onChange={setFocusMode}
        />

        <AccessibilityToggle
          icon="◐"
          title="High Contrast"
          description="Increase visual contrast"
          enabled={highContrast}
          onChange={setHighContrast}
        />

        <AccessibilityToggle
          icon="A+"
          title="Larger Text"
          description="Increase reading size"
          enabled={largerText}
          onChange={setLargerText}
        />

        <AccessibilityToggle
          icon="♫"
          title="Audio Narration"
          description="Listen while reading"
          enabled={narration}
          onChange={setNarration}
        />
      </div>

      {/* =====================================================
          ACTIVE SETTINGS
      ====================================================== */}
      <div className="mt-5 rounded-2xl border border-orange-100 bg-orange-50 p-4">
        <div className="flex items-center justify-between gap-3">
          <div>
            <p className="text-xs font-black text-orange-700">
              Active Settings
            </p>

            <p className="mt-0.5 text-[10px] text-orange-600/70">
              Your current learning preferences
            </p>
          </div>

          <span className="shrink-0 rounded-full bg-white px-2.5 py-1 text-[10px] font-black text-orange-600 shadow-sm">
            {activeCount}{' '}
            {activeCount === 1
              ? 'active'
              : 'active'}
          </span>
        </div>

        {activeCount > 0 ? (
          <div className="mt-3 flex flex-wrap gap-2">
            {activeSettings
              .filter((setting) => setting.enabled)
              .map((setting) => (
                <ActiveBadge
                  key={setting.label}
                  text={setting.label}
                />
              ))}
          </div>
        ) : (
          <p className="mt-3 rounded-xl bg-white/70 p-3 text-[11px] text-orange-700/70">
            No accessibility settings are currently enabled.
          </p>
        )}
      </div>

      {/* =====================================================
          RESET
      ====================================================== */}
      <button
        type="button"
        onClick={resetSettings}
        disabled={activeCount === 0}
        className={`mt-4 w-full rounded-xl border px-4 py-2.5 text-xs font-bold transition ${
          activeCount === 0
            ? 'cursor-not-allowed border-slate-100 bg-slate-50 text-slate-300'
            : 'border-slate-200 bg-white text-slate-500 hover:border-orange-200 hover:bg-orange-50 hover:text-orange-600'
        }`}
      >
        Reset Accessibility Settings
      </button>
    </div>
  )
}

function AccessibilityToggle({
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
      aria-pressed={enabled}
      className={`flex min-h-[64px] w-full items-center gap-3 rounded-2xl border p-3 text-left transition-all ${
        enabled
          ? 'border-orange-200 bg-orange-50'
          : 'border-transparent bg-slate-50 hover:border-slate-200 hover:bg-white'
      }`}
    >
      {/* Icon */}
      <div
        className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl text-xs font-black ${
          enabled
            ? 'bg-orange-500 text-white'
            : 'bg-white text-slate-500'
        }`}
      >
        {icon}
      </div>

      {/* Text */}
      <div className="min-w-0 flex-1">
        <p
          className={`text-xs font-black ${
            enabled
              ? 'text-orange-700'
              : 'text-slate-800'
          }`}
        >
          {title}
        </p>

        <p className="mt-0.5 truncate text-[10px] text-slate-500">
          {description}
        </p>
      </div>

      {/* Toggle */}
      <div
        className={`relative h-5 w-9 shrink-0 rounded-full transition-colors ${
          enabled
            ? 'bg-orange-500'
            : 'bg-slate-300'
        }`}
      >
        <span
          className={`absolute top-0.5 h-4 w-4 rounded-full bg-white shadow-sm transition-transform ${
            enabled
              ? 'translate-x-4'
              : 'translate-x-0.5'
          }`}
        />
      </div>
    </button>
  )
}

function ActiveBadge({ text }) {
  return (
    <span className="inline-flex items-center gap-1 rounded-lg bg-white px-2.5 py-1.5 text-[10px] font-bold text-orange-700 shadow-sm">
      <span>✓</span>
      {text}
    </span>
  )
}

export default AccessibilityPanel