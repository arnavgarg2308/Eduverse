import { useState } from 'react'

import TeacherLayout from '../../components/layout/TeacherLayout'

import {
  teacherProfile,
  teacherStats,
} from '../../data/teacherData'

function TeacherProfilePage() {
  const [name, setName] = useState(teacherProfile.name)
  const [email, setEmail] = useState(
    teacherProfile.email,
  )
  const [department, setDepartment] = useState(
    teacherProfile.department,
  )
  const [bio, setBio] = useState(
    teacherProfile.bio || '',
  )

  const [emailNotifications, setEmailNotifications] =
    useState(true)

  const [processingNotifications, setProcessingNotifications] =
    useState(true)

  const [saved, setSaved] = useState(false)

  const handleSave = () => {
    setSaved(true)

    setTimeout(() => {
      setSaved(false)
    }, 2500)
  }

  return (
    <TeacherLayout>
      <header className="border-b border-orange-100 bg-white">
        <div className="px-6 py-5 lg:px-8">
          <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
            EduVerse
          </p>

          <h1 className="mt-1 text-xl font-black text-slate-900">
            Teacher Profile
          </h1>
        </div>
      </header>

      <main className="px-6 py-8 lg:px-8">
        <div className="mx-auto max-w-5xl">
          {/* Intro */}
          <section>
            <p className="text-sm font-bold uppercase tracking-[0.15em] text-orange-500">
              Account Settings
            </p>

            <h2 className="mt-2 text-3xl font-black tracking-tight text-slate-900 sm:text-4xl">
              Your Teacher Profile
            </h2>

            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500 sm:text-base">
              Manage your EduVerse teacher information and workspace
              preferences.
            </p>
          </section>

          {/* Profile + Stats */}
          <section className="mt-8 grid gap-6 lg:grid-cols-[0.8fr_1.5fr]">
            {/* Profile Card */}
            <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex flex-col items-center text-center">
                <div className="flex h-24 w-24 items-center justify-center rounded-3xl bg-slate-900 text-2xl font-black text-white shadow-lg">
                  {getInitials(name)}
                </div>

                <h3 className="mt-5 text-xl font-black text-slate-900">
                  {name}
                </h3>

                <p className="mt-1 text-sm text-slate-500">
                  {department}
                </p>

                <span className="mt-4 rounded-full bg-orange-50 px-3 py-1.5 text-[10px] font-bold uppercase tracking-wider text-orange-600">
                  Teacher
                </span>
              </div>

              <div className="mt-8 grid grid-cols-2 gap-3">
                <StatItem
                  label="Content"
                  value={teacherStats.totalContent}
                />

                <StatItem
                  label="Students"
                  value={teacherStats.totalStudents}
                />

                <StatItem
                  label="Published"
                  value={teacherStats.publishedContent}
                />

                <StatItem
                  label="Engagement"
                  value={`${teacherStats.averageEngagement}%`}
                />
              </div>
            </div>

            {/* Personal Information */}
            <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
                Personal Information
              </p>

              <h3 className="mt-1 text-xl font-black text-slate-900">
                Profile Details
              </h3>

              <div className="mt-6 grid gap-5 sm:grid-cols-2">
                <InputField
                  label="Full Name"
                  value={name}
                  onChange={setName}
                />

                <InputField
                  label="Email Address"
                  value={email}
                  onChange={setEmail}
                  type="email"
                />

                <InputField
                  label="Department"
                  value={department}
                  onChange={setDepartment}
                />
              </div>

              <div className="mt-5">
                <label className="text-sm font-bold text-slate-800">
                  Bio
                </label>

                <textarea
                  value={bio}
                  onChange={(event) =>
                    setBio(event.target.value)
                  }
                  rows={4}
                  placeholder="Tell students a little about yourself..."
                  className="mt-2 w-full resize-none rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 outline-none transition placeholder:text-slate-400 focus:border-orange-400 focus:ring-2 focus:ring-orange-100"
                />
              </div>

              <div className="mt-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                {saved ? (
                  <p className="text-xs font-bold text-emerald-600">
                    ✓ Profile saved successfully
                  </p>
                ) : (
                  <span />
                )}

                <button
                  type="button"
                  onClick={handleSave}
                  className="rounded-xl bg-orange-500 px-5 py-3 text-xs font-bold text-white transition hover:bg-orange-600"
                >
                  Save Changes
                </button>
              </div>
            </div>
          </section>

          {/* Preferences */}
          <section className="mt-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
              Preferences
            </p>

            <h3 className="mt-1 text-xl font-black text-slate-900">
              Workspace Notifications
            </h3>

            <p className="mt-1 text-sm text-slate-500">
              Choose which updates EduVerse should send you.
            </p>

            <div className="mt-6 space-y-3">
              <PreferenceRow
                title="Email Notifications"
                description="Receive important updates about your EduVerse workspace."
                enabled={emailNotifications}
                onToggle={() =>
                  setEmailNotifications(
                    !emailNotifications,
                  )
                }
              />

              <PreferenceRow
                title="AI Processing Updates"
                description="Get notified when uploaded content finishes processing."
                enabled={processingNotifications}
                onToggle={() =>
                  setProcessingNotifications(
                    !processingNotifications,
                  )
                }
              />
            </div>
          </section>

          {/* Security */}
          <section className="mt-6 pb-8">
            <div className="rounded-3xl border border-orange-100 bg-gradient-to-r from-orange-50 to-amber-50 p-6">
              <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
                Account Security
              </p>

              <h3 className="mt-1 text-xl font-black text-slate-900">
                Keep your account secure.
              </h3>

              <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">
                Password management and authentication controls will
                be connected to the EduVerse backend.
              </p>

              <button
                type="button"
                className="mt-5 rounded-xl border border-slate-200 bg-white px-5 py-3 text-xs font-bold text-slate-600 transition hover:border-orange-200 hover:bg-orange-50 hover:text-orange-600"
              >
                Change Password
              </button>
            </div>
          </section>
        </div>
      </main>
    </TeacherLayout>
  )
}

function InputField({
  label,
  value,
  onChange,
  type = 'text',
}) {
  return (
    <div>
      <label className="text-sm font-bold text-slate-800">
        {label}
      </label>

      <input
        type={type}
        value={value}
        onChange={(event) =>
          onChange(event.target.value)
        }
        className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 outline-none transition focus:border-orange-400 focus:ring-2 focus:ring-orange-100"
      />
    </div>
  )
}

function StatItem({ label, value }) {
  return (
    <div className="rounded-2xl bg-slate-50 p-4">
      <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
        {label}
      </p>

      <p className="mt-1 text-lg font-black text-slate-800">
        {value}
      </p>
    </div>
  )
}

function PreferenceRow({
  title,
  description,
  enabled,
  onToggle,
}) {
  return (
    <div className="flex items-center justify-between gap-5 rounded-2xl border border-slate-100 bg-slate-50 p-4">
      <div>
        <h4 className="text-sm font-bold text-slate-800">
          {title}
        </h4>

        <p className="mt-1 text-xs leading-5 text-slate-500">
          {description}
        </p>
      </div>

      <button
        type="button"
        onClick={onToggle}
        aria-label={`Toggle ${title}`}
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
  )
}

function getInitials(value) {
  return value
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0])
    .join('')
    .toUpperCase()
}

export default TeacherProfilePage