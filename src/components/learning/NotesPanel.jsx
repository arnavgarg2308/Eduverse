import { useState } from 'react'

function NotesPanel({ course }) {
  const concepts = [
    {
      title: 'What are Data Structures?',
      text: 'Data structures are organized ways of storing and managing data so that it can be accessed and modified efficiently.',
    },
    {
      title: 'Why do we need them?',
      text: 'Choosing the right data structure can make a program faster, easier to understand and more memory efficient.',
    },
    {
      title: 'Common examples',
      text: 'Arrays, linked lists, stacks, queues, trees and graphs are some commonly used data structures.',
    },
  ]

  const keyPoints = [
    'Data structures organize information for efficient use.',
    'Different problems require different data structures.',
    'The choice of structure affects performance.',
    'Arrays and linked lists are fundamental linear structures.',
  ]

  const [saved, setSaved] = useState(false)

  const handleSave = () => {
    setSaved(true)

    setTimeout(() => {
      setSaved(false)
    }, 2000)
  }

  return (
    <div className="mt-6 grid gap-6 lg:grid-cols-[1.5fr_0.8fr]">
      {/* =====================================================
          MAIN NOTES
      ====================================================== */}
      <article className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
        {/* Header */}
        <div className="flex flex-col gap-4 border-b border-slate-100 pb-6 sm:flex-row sm:items-start sm:justify-between">
          <div className="min-w-0">
            <div className="inline-flex items-center gap-2 rounded-lg bg-orange-50 px-3 py-1.5 text-xs font-bold text-orange-600">
              <span>✦</span>
              AI Simplified Notes
            </div>

            <h2 className="mt-4 break-words text-2xl font-black text-slate-900">
              {course?.title || 'Lesson Notes'}
            </h2>

            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">
              A simplified explanation of the key concepts from this
              lesson.
            </p>
          </div>

          <button
            type="button"
            onClick={handleSave}
            className={`shrink-0 rounded-xl border px-4 py-2.5 text-xs font-bold transition ${
              saved
                ? 'border-emerald-200 bg-emerald-50 text-emerald-600'
                : 'border-slate-200 text-slate-600 hover:border-orange-200 hover:bg-orange-50 hover:text-orange-600'
            }`}
          >
            {saved ? '✓ Notes Saved' : 'Save Notes'}
          </button>
        </div>

        {/* Concepts */}
        <div className="mt-7 space-y-7">
          {concepts.map((concept, index) => (
            <section
              key={concept.title}
              className="group"
            >
              <div className="flex items-start gap-4">
                <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-orange-50 text-xs font-black text-orange-600 transition group-hover:bg-orange-500 group-hover:text-white">
                  {String(index + 1).padStart(2, '0')}
                </span>

                <div className="min-w-0">
                  <h3 className="text-base font-black text-slate-900">
                    {concept.title}
                  </h3>

                  <p className="mt-2 text-sm leading-7 text-slate-600">
                    {concept.text}
                  </p>
                </div>
              </div>
            </section>
          ))}
        </div>

        {/* Summary */}
        <div className="mt-8 rounded-2xl border border-orange-100 bg-gradient-to-br from-orange-50 to-amber-50 p-5 sm:p-6">
          <div className="flex items-center gap-2">
            <span className="text-orange-500">
              ✦
            </span>

            <h3 className="text-sm font-black text-slate-900">
              In simple words
            </h3>
          </div>

          <p className="mt-3 text-sm leading-7 text-slate-600">
            Think of a data structure as a smart container for your
            information. The right container makes it easier and faster
            to find, add, remove or organize the data you need.
          </p>
        </div>

        {/* Notes Footer */}
        <div className="mt-6 flex flex-col gap-3 rounded-2xl border border-slate-100 bg-slate-50 p-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-xs font-bold text-slate-700">
              AI-generated study notes
            </p>

            <p className="mt-1 text-[11px] text-slate-400">
              Review these notes before taking the knowledge check.
            </p>
          </div>

          <span className="w-fit rounded-lg bg-white px-3 py-1.5 text-[10px] font-bold uppercase tracking-wider text-orange-500 ring-1 ring-slate-100">
            {concepts.length} concepts
          </span>
        </div>
      </article>

      {/* =====================================================
          SIDEBAR
      ====================================================== */}
      <aside className="space-y-5">
        {/* Key Points */}
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-orange-50 text-orange-600">
              ✓
            </div>

            <div>
              <h3 className="font-black text-slate-900">
                Key Points
              </h3>

              <p className="text-xs text-slate-500">
                Remember these concepts
              </p>
            </div>
          </div>

          <div className="mt-5 space-y-4">
            {keyPoints.map((point, index) => (
              <div
                key={point}
                className="flex gap-3"
              >
                <span className="mt-2 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-orange-50 text-[9px] font-black text-orange-600">
                  {index + 1}
                </span>

                <p className="text-sm leading-6 text-slate-600">
                  {point}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Study Tip */}
        <div className="overflow-hidden rounded-3xl bg-gradient-to-br from-slate-900 to-slate-800 p-6 text-white shadow-lg">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-orange-500 text-white">
            💡
          </div>

          <p className="mt-5 text-xs font-bold uppercase tracking-wider text-orange-400">
            Study Tip
          </p>

          <h3 className="mt-2 text-lg font-black">
            Learn → Recall → Practice
          </h3>

          <p className="mt-2 text-sm leading-6 text-slate-400">
            After reading the explanation, try the quiz to check how
            much you can remember without looking at your notes.
          </p>

          <div className="mt-5 flex items-center gap-2 text-xs font-semibold text-slate-300">
            <span className="rounded-lg bg-white/5 px-2.5 py-1.5">
              1. Learn
            </span>

            <span className="text-orange-400">
              →
            </span>

            <span className="rounded-lg bg-white/5 px-2.5 py-1.5">
              2. Recall
            </span>

            <span className="text-orange-400">
              →
            </span>

            <span className="rounded-lg bg-white/5 px-2.5 py-1.5">
              3. Practice
            </span>
          </div>
        </div>
      </aside>
    </div>
  )
}

export default NotesPanel