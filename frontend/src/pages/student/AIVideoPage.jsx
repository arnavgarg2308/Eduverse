import { useState } from 'react'

import DashboardLayout from '../../components/layout/DashboardLayout'
import AIVideoUpload from '../../components/student/AIVideoUpload'

function AIVideoPage() {
  const [file, setFile] = useState(null)
const [narration, setNarration] = useState(true)
const [subtitles, setSubtitles] = useState(true)
const [generating, setGenerating] = useState(false)
const [generated, setGenerated] = useState(false)
const [analysisResult, setAnalysisResult] = useState(null)
const [error, setError] = useState('')
  const handleGenerate = async () => {
  if (!file) return

  setGenerating(true)
  setGenerated(false)
  setAnalysisResult(null)
  setError('')

  try {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch('http://127.0.0.1:8001/analyze', {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      const errorData = await response.json()

      throw new Error(
        errorData.detail || 'Failed to analyze PDF'
      )
    }

    const result = await response.json()

    console.log('EduMorph Analysis Result:', result)

    setAnalysisResult(result)
    setGenerated(true)

  } catch (err) {
    console.error(err)
    setError(err.message)

  } finally {
    setGenerating(false)
  }
}

  return (
    <DashboardLayout>
      <div className="min-h-screen bg-slate-50">

        {/* HEADER */}
        <div className="border-b border-slate-200 bg-white px-5 py-5 sm:px-8">
          <div className="mx-auto max-w-7xl">
            <p className="text-xs font-black uppercase tracking-[0.18em] text-orange-500">
              EduVerse
            </p>

            <h1 className="mt-1 text-2xl font-black text-slate-900">
              AI Video Generator
            </h1>

            <p className="mt-1 text-sm text-slate-500">
              Turn your study material into an engaging learning video.
            </p>
          </div>
        </div>

        {/* CONTENT */}
        <div className="mx-auto max-w-7xl px-5 py-6 sm:px-8">

          <div className="grid gap-6 lg:grid-cols-[1.3fr_0.7fr]">

            {/* LEFT */}
            <div className="space-y-6">

              <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">

                <div className="flex items-start gap-4">

                  <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-orange-50 text-xl text-orange-500">
                    ↑
                  </div>

                  <div>
                    <h2 className="text-lg font-black text-slate-900">
                      Upload Your Study Material
                    </h2>

                    <p className="mt-1 text-sm leading-6 text-slate-500">
                      Upload lecture notes, textbook pages,
                      assignments or other learning material.
                    </p>
                  </div>

                </div>

                <div className="mt-6">
                  <AIVideoUpload
                    onFileSelected={(selectedFile) => {
                      setFile(selectedFile)
                      setGenerated(false)
                    }}
                  />
                </div>

              </div>

              {/* HOW IT WORKS */}
              <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">

                <div className="flex items-center gap-3">

                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-orange-50 text-orange-500">
                    ✦
                  </div>

                  <div>
                    <h2 className="font-black text-slate-900">
                      How It Works
                    </h2>

                    <p className="text-xs text-slate-500">
                      From study material to learning video.
                    </p>
                  </div>

                </div>

                <div className="mt-6 grid gap-4 sm:grid-cols-3">

                  <Step
                    number="01"
                    title="Upload"
                    text="Upload your PDF or study image."
                  />

                  <Step
                    number="02"
                    title="AI Understands"
                    text="EduVerse analyzes your learning material."
                  />

                  <Step
                    number="03"
                    title="Video Creation"
                    text="Your content becomes a visual lesson."
                  />

                </div>

              </div>

            </div>

            {/* RIGHT */}
            <div className="space-y-6">

              {/* NARRATION */}
              <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">

                <p className="text-xs font-black uppercase tracking-wider text-orange-500">
                  Audio
                </p>

                <div className="mt-3 flex items-center justify-between gap-4">

                  <div>
                    <h2 className="text-lg font-black text-slate-900">
                      Voice Narration
                    </h2>

                    <p className="mt-1 text-sm leading-6 text-slate-500">
                      Add AI narration to your learning video.
                    </p>
                  </div>

                  <Toggle
                    value={narration}
                    onChange={() => setNarration(!narration)}
                  />

                </div>

              </div>

              {/* SUBTITLES AT END */}
              <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">

                <p className="text-xs font-black uppercase tracking-wider text-orange-500">
                  Accessibility
                </p>

                <div className="mt-3 flex items-center justify-between gap-4">

                  <div>
                    <h2 className="text-lg font-black text-slate-900">
                      Subtitles
                    </h2>

                    <p className="mt-1 text-sm leading-6 text-slate-500">
                      Display subtitles in the generated video.
                    </p>
                  </div>

                  <Toggle
                    value={subtitles}
                    onChange={() => setSubtitles(!subtitles)}
                  />

                </div>

              </div>

              {/* GENERATE */}
              <div className="rounded-3xl bg-slate-900 p-6 text-white shadow-lg">

                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-orange-500">
                  ✦
                </div>

                <h2 className="mt-5 text-xl font-black">
                  Ready to Generate?
                </h2>

                <p className="mt-2 text-sm leading-6 text-slate-400">
                  Upload your study material and let EduVerse
                  create your learning video.
                </p>

                <button
                  type="button"
                  disabled={!file || generating}
                  onClick={handleGenerate}
                  className={`mt-6 w-full rounded-xl px-5 py-3.5 text-sm font-black transition ${
                    !file || generating
                      ? 'cursor-not-allowed bg-slate-700 text-slate-500'
                      : 'bg-orange-500 text-white hover:bg-orange-400'
                  }`}
                >
                  {generating
                    ? 'Creating Video...'
                    : 'Generate AI Video →'}
                </button>

              </div>

              {/* GENERATED VIDEO */}
             {generated && analysisResult && (
  <div className="rounded-3xl border border-emerald-200 bg-emerald-50 p-6">

    <div className="flex items-center gap-3">
      <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500 text-white">
        ✓
      </div>

      <div>
        <h3 className="font-black text-emerald-800">
          Analysis Complete
        </h3>

        <p className="text-xs text-emerald-700">
          Your PDF has been analyzed successfully.
        </p>
      </div>
    </div>

    <pre className="mt-5 max-h-96 overflow-auto rounded-2xl bg-slate-900 p-4 text-xs text-green-400">
      {JSON.stringify(analysisResult, null, 2)}
    </pre>

  </div>
)}

            </div>

          </div>

        </div>

      </div>
    </DashboardLayout>
  )
}

function Toggle({ value, onChange }) {
  return (
    <button
      type="button"
      onClick={onChange}
      aria-pressed={value}
      className={`relative h-7 w-12 shrink-0 rounded-full transition ${
        value
          ? 'bg-orange-500'
          : 'bg-slate-300'
      }`}
    >
      <span
        className={`absolute top-1 h-5 w-5 rounded-full bg-white shadow transition ${
          value
            ? 'translate-x-6'
            : 'translate-x-1'
        }`}
      />
    </button>
  )
}

function Step({ number, title, text }) {
  return (
    <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">

      <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-orange-50 text-[10px] font-black text-orange-600">
        {number}
      </span>

      <h3 className="mt-4 text-sm font-black text-slate-900">
        {title}
      </h3>

      <p className="mt-1 text-xs leading-5 text-slate-500">
        {text}
      </p>

    </div>
  )
}

export default AIVideoPage