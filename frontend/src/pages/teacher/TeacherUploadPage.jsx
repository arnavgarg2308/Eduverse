import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import TeacherLayout from '../../components/layout/TeacherLayout'
import UploadDropzone from '../../components/teacher/UploadDropzone'
import UploadConfiguration from '../../components/teacher/UploadConfiguration'

import {
  uploadLanguages,
  uploadAccessibilityOptions,
  uploadCategories,
  uploadDifficultyLevels,
} from '../../data/uploadData'

function TeacherUploadPage() {
  const navigate = useNavigate()

  const [selectedFile, setSelectedFile] = useState(null)

  const [category, setCategory] = useState(
    uploadCategories[0],
  )

  const [difficulty, setDifficulty] = useState(
    uploadDifficultyLevels[1],
  )

  const [language, setLanguage] = useState(
    uploadLanguages[0].name,
  )

  const [accessibilityOptions, setAccessibilityOptions] =
    useState(uploadAccessibilityOptions)

  const [isSubmitting, setIsSubmitting] = useState(false)

  const [submitMessage, setSubmitMessage] = useState('')

  const handleAccessibilityToggle = (id) => {
    setAccessibilityOptions((current) =>
      current.map((option) =>
        option.id === id
          ? {
              ...option,
              enabled: !option.enabled,
            }
          : option,
      ),
    )
  }

  const handleGenerate = () => {
    if (!selectedFile) {
      setSubmitMessage(
        'Please upload a learning file before continuing.',
      )

      return
    }

    setSubmitMessage('')
    setIsSubmitting(true)

    // Temporary frontend demo.
    // Backend/API integration will be connected later.

    setTimeout(() => {
      setIsSubmitting(false)

      setSubmitMessage(
        'Content submitted successfully. AI processing will begin once the backend is connected.',
      )
    }, 1200)
  }

  return (
    <TeacherLayout>
      {/* =====================================================
          HEADER
      ====================================================== */}
      <header className="border-b border-orange-100 bg-white">
        <div className="flex items-center justify-between px-6 py-5 lg:px-8">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
              EduVerse
            </p>

            <h1 className="mt-1 text-xl font-black text-slate-900">
              Upload Learning Content
            </h1>
          </div>

          <button
            type="button"
            onClick={() =>
              navigate('/teacher/dashboard')
            }
            className="rounded-xl border border-slate-200 px-4 py-2.5 text-xs font-bold text-slate-600 transition hover:border-orange-200 hover:bg-orange-50 hover:text-orange-600"
          >
            ← Dashboard
          </button>
        </div>
      </header>

      {/* =====================================================
          MAIN
      ====================================================== */}
      <main className="px-6 py-8 lg:px-8">
        <div className="mx-auto max-w-5xl">
          {/* =================================================
              INTRO
          ================================================== */}
          <section>
            <p className="text-sm font-bold uppercase tracking-[0.15em] text-orange-500">
              AI Content Studio
            </p>

            <h2 className="mt-2 text-3xl font-black tracking-tight text-slate-900 sm:text-4xl">
              Turn your content into personalized learning.
            </h2>

            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500 sm:text-base">
              Upload your educational material and choose how EduVerse
              should transform it for your students.
            </p>
          </section>

          {/* =================================================
              STEP 1
          ================================================== */}
          <section className="mt-8">
            <StepHeader
              number="01"
              title="Upload your content"
              description="Start with a PDF, presentation or study notes."
            />

            <div className="mt-4 rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
              <UploadDropzone
                selectedFile={selectedFile}
                onFileSelect={setSelectedFile}
              />
            </div>
          </section>

          {/* =================================================
              STEP 2
          ================================================== */}
          <section className="mt-10">
            <StepHeader
              number="02"
              title="Configure AI learning outputs"
              description="Choose how your content should be transformed."
            />

            <div className="mt-4">
              <UploadConfiguration
                category={category}
                difficulty={difficulty}
                language={language}
                categories={uploadCategories}
                difficultyLevels={uploadDifficultyLevels}
                languages={uploadLanguages}
                accessibilityOptions={accessibilityOptions}
                onCategoryChange={setCategory}
                onDifficultyChange={setDifficulty}
                onLanguageChange={setLanguage}
                onAccessibilityToggle={
                  handleAccessibilityToggle
                }
              />
            </div>
          </section>

          {/* =================================================
              FILE SUMMARY
          ================================================== */}
          {selectedFile && (
            <section className="mt-10">
              <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
                  <div className="min-w-0">
                    <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
                      Ready to Process
                    </p>

                    <h3 className="mt-1 truncate text-lg font-black text-slate-900">
                      {selectedFile.name}
                    </h3>

                    <p className="mt-1 text-xs text-slate-500">
                      {category} • {difficulty} • {language}
                    </p>
                  </div>

                  <div className="shrink-0 rounded-2xl bg-orange-50 px-5 py-3 text-center">
                    <p className="text-[10px] font-bold uppercase tracking-wider text-orange-500">
                      AI Outputs
                    </p>

                    <p className="mt-1 text-lg font-black text-orange-700">
                      {
                        accessibilityOptions.filter(
                          (option) => option.enabled,
                        ).length
                      }
                    </p>
                  </div>
                </div>
              </div>
            </section>
          )}

          {/* =================================================
              STEP 3
          ================================================== */}
          <section className="mt-8 pb-10">
            <div className="overflow-hidden rounded-3xl bg-gradient-to-r from-orange-500 to-amber-500 p-6 text-white shadow-xl shadow-orange-100 sm:p-8">
              <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
                <div className="max-w-xl">
                  <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-100">
                    Ready?
                  </p>

                  <h3 className="mt-2 text-xl font-black sm:text-2xl">
                    Generate your learning experience.
                  </h3>

                  <p className="mt-2 text-sm leading-6 text-orange-50">
                    EduVerse will analyze your content and prepare the
                    selected learning formats.
                  </p>

                  <div className="mt-4 flex flex-wrap gap-2">
                    {accessibilityOptions
                      .filter((option) => option.enabled)
                      .map((option) => (
                        <span
                          key={option.id}
                          className="rounded-lg bg-white/15 px-2.5 py-1.5 text-[10px] font-bold text-white backdrop-blur-sm"
                        >
                          ✓ {option.title}
                        </span>
                      ))}
                  </div>
                </div>

                <button
                  type="button"
                  onClick={handleGenerate}
                  disabled={isSubmitting}
                  className="shrink-0 rounded-2xl bg-white px-6 py-3.5 text-sm font-black text-orange-600 shadow-lg transition hover:bg-orange-50 disabled:cursor-not-allowed disabled:opacity-70"
                >
                  {isSubmitting
                    ? 'Preparing...'
                    : 'Generate Learning Content →'}
                </button>
              </div>
            </div>

            {/* Status */}
            {submitMessage && (
              <div
                className={`mt-4 rounded-2xl border px-4 py-3 text-sm font-semibold ${
                  submitMessage.includes('successfully')
                    ? 'border-emerald-100 bg-emerald-50 text-emerald-700'
                    : 'border-orange-100 bg-orange-50 text-orange-700'
                }`}
              >
                {submitMessage}
              </div>
            )}
          </section>
        </div>
      </main>
    </TeacherLayout>
  )
}

function StepHeader({
  number,
  title,
  description,
}) {
  return (
    <div className="flex items-start gap-4">
      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-orange-500 text-xs font-black text-white shadow-sm">
        {number}
      </div>

      <div>
        <h3 className="text-lg font-black text-slate-900">
          {title}
        </h3>

        <p className="mt-1 text-sm text-slate-500">
          {description}
        </p>
      </div>
    </div>
  )
}

export default TeacherUploadPage