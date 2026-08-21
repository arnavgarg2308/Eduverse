import { useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'

import DashboardLayout from '../../components/layout/DashboardLayout'
import LearningHeader from '../../components/learning/LearningHeader'
import VideoPlayer from '../../components/learning/VideoPlayer'
import LearningTabs from '../../components/learning/LearningTabs'
import NotesPanel from '../../components/learning/NotesPanel'
import LanguageSelector from '../../components/learning/LanguageSelector'
import AccessibilityPanel from '../../components/learning/AccessibilityPanel'

import { libraryCourses } from '../../data/libraryData'

function LearningPage() {
  const { courseId } = useParams()
  const navigate = useNavigate()

  const course = libraryCourses.find(
    (item) => item.id === courseId,
  )

  const currentCourse = course || libraryCourses[0]

  const [activeTab, setActiveTab] = useState('video')

  const [selectedLanguage, setSelectedLanguage] =
    useState(
      currentCourse?.language || 'English',
    )

  const [selectedAnswer, setSelectedAnswer] =
    useState(null)

  const [quizStarted, setQuizStarted] =
    useState(false)

  if (!currentCourse) {
    return (
      <DashboardLayout
        role="student"
        title="Learning"
      >
        <EmptyLearningState
          onBack={() =>
            navigate('/student/library')
          }
        />
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout
      role="student"
      title="Learning"
    >
      <div className="mx-auto max-w-7xl">
        {/* =================================================
            TOP NAV
        ================================================== */}
        <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
          <button
            type="button"
            onClick={() =>
              navigate('/student/library')
            }
            className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs font-bold text-slate-600 transition hover:border-orange-200 hover:bg-orange-50 hover:text-orange-600"
          >
            ← Back to Library
          </button>

          {courseId &&
            !course && (
              <span className="rounded-xl bg-amber-50 px-3 py-2 text-[10px] font-bold uppercase tracking-wider text-amber-600">
                Showing recommended course
              </span>
            )}
        </div>

        {/* =================================================
            COURSE HEADER
        ================================================== */}
        <LearningHeader
          course={currentCourse}
        />

        {/* =================================================
            PROGRESS
        ================================================== */}
        <section className="mt-5 rounded-2xl border border-orange-100 bg-orange-50/70 p-4">
          <div className="flex items-center justify-between gap-4">
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-orange-600">
                Learning Progress
              </p>

              <p className="mt-1 text-sm font-bold text-slate-900">
                Keep going — you're making progress.
              </p>
            </div>

            <span className="text-sm font-black text-orange-600">
              32%
            </span>
          </div>

          <div className="mt-3 h-2 overflow-hidden rounded-full bg-white">
            <div className="h-full w-[32%] rounded-full bg-gradient-to-r from-orange-500 to-amber-400" />
          </div>
        </section>

        {/* =================================================
            MAIN LEARNING CONTENT
        ================================================== */}
        <section className="mt-6">
          {activeTab === 'video' && (
            <VideoPlayer
              title={currentCourse.title}
              duration={currentCourse.duration}
            />
          )}

          {activeTab === 'audio' && (
            <AudioPlaceholder
              course={currentCourse}
            />
          )}

          {activeTab === 'notes' && (
            <NotesPanel
              course={currentCourse}
            />
          )}

          {activeTab === 'quiz' && (
            <QuizPlaceholder
              course={currentCourse}
              selectedAnswer={selectedAnswer}
              onAnswerSelect={setSelectedAnswer}
              quizStarted={quizStarted}
              onStart={() => setQuizStarted(true)}
            />
          )}
        </section>

        {/* =================================================
            TABS
        ================================================== */}
        <section className="mt-5">
          <LearningTabs
            activeTab={activeTab}
            onTabChange={(tab) => {
              setActiveTab(tab)
              setSelectedAnswer(null)
            }}
          />
        </section>

        {/* =================================================
            SUPPORTING CONTROLS
        ================================================== */}
        <section className="mt-6 grid gap-6 pb-8 lg:grid-cols-2">
          <LanguageSelector
            selectedLanguage={selectedLanguage}
            onLanguageChange={setSelectedLanguage}
          />

          <AccessibilityPanel />
        </section>

        {/* =================================================
            COMPLETION CTA
        ================================================== */}
        <section className="pb-10">
          <div className="overflow-hidden rounded-3xl bg-slate-900 p-6 text-white shadow-xl sm:p-8">
            <div className="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-400">
                  EduVerse Learning
                </p>

                <h3 className="mt-2 text-xl font-black sm:text-2xl">
                  Ready to finish this lesson?
                </h3>

                <p className="mt-1 max-w-xl text-sm leading-6 text-slate-400">
                  Complete the lesson and test your understanding with
                  the knowledge check.
                </p>
              </div>

              <button
                type="button"
                onClick={() => {
                  setActiveTab('quiz')
                  setQuizStarted(true)
                }}
                className="shrink-0 rounded-xl bg-orange-500 px-5 py-3 text-sm font-bold text-white transition hover:bg-orange-600"
              >
                Take Knowledge Check →
              </button>
            </div>
          </div>
        </section>
      </div>
    </DashboardLayout>
  )
}

/* =========================================================
   AUDIO PLACEHOLDER
========================================================= */

function AudioPlaceholder({ course }) {
  return (
    <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
      <div className="bg-gradient-to-br from-purple-50 via-white to-orange-50 p-6 sm:p-10">
        <div className="mx-auto max-w-2xl text-center">
          <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-3xl bg-gradient-to-br from-purple-500 to-violet-500 text-3xl text-white shadow-xl shadow-purple-200">
            ♫
          </div>

          <p className="mt-6 text-xs font-bold uppercase tracking-[0.18em] text-purple-500">
            Audio Learning
          </p>

          <h2 className="mt-3 text-2xl font-black text-slate-900 sm:text-3xl">
            Listen to {course.title}
          </h2>

          <p className="mx-auto mt-3 max-w-xl text-sm leading-6 text-slate-500">
            Listen to the lesson narration while following along with
            the transcript.
          </p>

          <div className="mt-8 rounded-3xl bg-slate-900 p-5 text-left shadow-xl">
            <div className="flex items-center gap-4">
              <button
                type="button"
                className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-purple-500 text-white transition hover:bg-purple-600"
              >
                ▶
              </button>

              <div className="flex-1">
                <div className="h-2 overflow-hidden rounded-full bg-white/10">
                  <div className="h-full w-[32%] rounded-full bg-gradient-to-r from-purple-500 to-violet-400" />
                </div>

                <div className="mt-2 flex justify-between text-[10px] text-slate-500">
                  <span>03:42</span>
                  <span>{course.duration}</span>
                </div>
              </div>

              <button
                type="button"
                className="hidden text-sm text-slate-400 transition hover:text-white sm:block"
                aria-label="Audio volume"
              >
                🔊
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Transcript */}
      <div className="border-t border-slate-100 p-6 sm:p-8">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <p className="text-xs font-bold uppercase tracking-wider text-purple-500">
              Transcript
            </p>

            <h3 className="mt-1 text-lg font-black text-slate-900">
              Follow along
            </h3>
          </div>

          <span className="rounded-lg bg-purple-50 px-3 py-1.5 text-xs font-bold text-purple-600">
            {course.language}
          </span>
        </div>

        <p className="mt-5 max-w-3xl text-sm leading-7 text-slate-600">
          Welcome to this lesson. In this section, we will explore the
          core concepts, build an intuitive understanding and then
          move into examples and practical applications.
        </p>
      </div>
    </div>
  )
}

/* =========================================================
   QUIZ
========================================================= */

function QuizPlaceholder({
  course,
  selectedAnswer,
  onAnswerSelect,
  quizStarted,
  onStart,
}) {
  const options = [
    'Array',
    'Linked List',
    'Graph',
    'Tree',
  ]

  if (!quizStarted) {
    return (
      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
        <div className="flex flex-col gap-6 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <div className="inline-flex items-center gap-2 rounded-lg bg-blue-50 px-3 py-1.5 text-xs font-bold text-blue-600">
              ✓ Knowledge Check
            </div>

            <h2 className="mt-4 text-2xl font-black text-slate-900 sm:text-3xl">
              Test what you learned.
            </h2>

            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">
              Answer a few questions based on{' '}
              {course.title} to check your understanding.
            </p>
          </div>

          <div className="rounded-2xl bg-blue-50 px-5 py-4 text-center">
            <p className="text-xs font-bold text-blue-500">
              Questions
            </p>

            <p className="mt-1 text-xl font-black text-blue-700">
              10
            </p>
          </div>
        </div>

        <div className="mt-8 rounded-2xl bg-slate-50 p-6">
          <p className="text-sm leading-6 text-slate-600">
            Take a short knowledge check after completing the lesson.
            Your answers can be used to identify topics that need
            more practice.
          </p>
        </div>

        <div className="mt-6 flex justify-end">
          <button
            type="button"
            onClick={onStart}
            className="rounded-xl bg-blue-500 px-5 py-3 text-sm font-bold text-white transition hover:bg-blue-600"
          >
            Start Quiz →
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
      <div className="flex flex-col gap-5 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <div className="inline-flex items-center gap-2 rounded-lg bg-blue-50 px-3 py-1.5 text-xs font-bold text-blue-600">
            ✓ Question 01
          </div>

          <h2 className="mt-4 text-2xl font-black text-slate-900">
            Which data structure is commonly used to store elements
            in contiguous memory locations?
          </h2>
        </div>

        <div className="shrink-0 rounded-2xl bg-blue-50 px-4 py-3 text-center">
          <p className="text-[10px] font-bold uppercase tracking-wider text-blue-500">
            Progress
          </p>

          <p className="mt-1 text-lg font-black text-blue-700">
            1 / 10
          </p>
        </div>
      </div>

      <div className="mt-7 grid gap-3 sm:grid-cols-2">
        {options.map((option) => {
          const selected =
            selectedAnswer === option

          return (
            <button
              key={option}
              type="button"
              onClick={() =>
                onAnswerSelect(option)
              }
              className={`rounded-2xl border p-4 text-left text-sm font-bold transition ${
                selected
                  ? 'border-blue-400 bg-blue-50 text-blue-700 ring-2 ring-blue-100'
                  : 'border-slate-200 bg-white text-slate-700 hover:border-blue-300 hover:bg-blue-50 hover:text-blue-700'
              }`}
            >
              <div className="flex items-center justify-between gap-3">
                <span>{option}</span>

                {selected && (
                  <span className="text-blue-600">
                    ✓
                  </span>
                )}
              </div>
            </button>
          )
        })}
      </div>

      <div className="mt-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <p className="text-xs text-slate-400">
          Select an answer to continue.
        </p>

        <button
          type="button"
          disabled={!selectedAnswer}
          className={`rounded-xl px-5 py-3 text-sm font-bold transition ${
            selectedAnswer
              ? 'bg-blue-500 text-white hover:bg-blue-600'
              : 'cursor-not-allowed bg-slate-100 text-slate-400'
          }`}
        >
          Submit Answer →
        </button>
      </div>
    </div>
  )
}

/* =========================================================
   EMPTY STATE
========================================================= */

function EmptyLearningState({ onBack }) {
  return (
    <div className="flex min-h-[60vh] items-center justify-center">
      <div className="max-w-md rounded-3xl border border-slate-200 bg-white p-8 text-center shadow-sm">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-orange-50 text-2xl">
          📚
        </div>

        <h2 className="mt-5 text-xl font-black text-slate-900">
          Course not found
        </h2>

        <p className="mt-2 text-sm leading-6 text-slate-500">
          We couldn't find the learning content you requested.
          Return to the library and choose a course.
        </p>

        <button
          type="button"
          onClick={onBack}
          className="mt-6 rounded-xl bg-orange-500 px-5 py-3 text-sm font-bold text-white transition hover:bg-orange-600"
        >
          Back to Library
        </button>
      </div>
    </div>
  )
}

export default LearningPage