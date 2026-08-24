import { useState } from 'react'

import DashboardLayout from '../../components/layout/DashboardLayout'
import ProfileCard from '../../components/profile/ProfileCard'
import LearningPreferences from '../../components/profile/LearningPreferences'
import AccessibilityPreferences from '../../components/profile/AccessibilityPreferences'
import NotificationPreferences from '../../components/profile/NotificationPreferences'

import {
  profileData,
  learningPreferences,
  supportedLearningLanguages,
  learningModes,
  accessibilityPreferences,
  notificationPreferences,
} from '../../data/profileData'

function ProfilePage() {
  const [preferences, setPreferences] = useState(
    learningPreferences,
  )

  const [accessibility, setAccessibility] = useState(
    accessibilityPreferences,
  )

  const [notifications, setNotifications] = useState(
    notificationPreferences,
  )

  const handleLanguageChange = (language) => {
    setPreferences((current) => ({
      ...current,
      language,
    }))
  }

  const handleModeChange = (learningMode) => {
    setPreferences((current) => ({
      ...current,
      learningMode,
    }))
  }

  const handleAccessibilityToggle = (id) => {
    setAccessibility((current) =>
      current.map((item) =>
        item.id === id
          ? {
              ...item,
              enabled: !item.enabled,
            }
          : item,
      ),
    )
  }

  const handleNotificationToggle = (id) => {
    setNotifications((current) =>
      current.map((item) =>
        item.id === id
          ? {
              ...item,
              enabled: !item.enabled,
            }
          : item,
      ),
    )
  }

  return (
    <DashboardLayout role="student" title="Profile & Settings">
      {/* =====================================================
          PAGE HEADER
      ====================================================== */}
      <section>
        <p className="text-sm font-bold uppercase tracking-[0.15em] text-orange-500">
          Account
        </p>

        <h1 className="mt-2 text-3xl font-black tracking-tight text-slate-900 sm:text-4xl">
          Profile & Settings
        </h1>

        <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500 sm:text-base">
          Personalize your EduMorph experience and choose how you
          want to learn.
        </p>
      </section>

      {/* =====================================================
          PROFILE
      ====================================================== */}
      <section className="mt-8">
        <ProfileCard profile={profileData} />
      </section>

      {/* =====================================================
          LEARNING PREFERENCES
      ====================================================== */}
      <section className="mt-6">
        <LearningPreferences
          preferences={preferences}
          languages={supportedLearningLanguages}
          modes={learningModes}
          onLanguageChange={handleLanguageChange}
          onModeChange={handleModeChange}
        />
      </section>

      {/* =====================================================
          ACCESSIBILITY + NOTIFICATIONS
      ====================================================== */}
      <section className="mt-6 grid gap-6 xl:grid-cols-2">
        <AccessibilityPreferences
          preferences={accessibility}
          onToggle={handleAccessibilityToggle}
        />

        <NotificationPreferences
          preferences={notifications}
          onToggle={handleNotificationToggle}
        />
      </section>

      {/* =====================================================
          SAVE / STATUS
      ====================================================== */}
      <section className="mt-6 pb-8">
        <div className="flex flex-col gap-4 rounded-3xl border border-orange-100 bg-gradient-to-r from-orange-50 to-amber-50 p-5 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-sm font-bold text-slate-900">
              Your preferences are ready.
            </p>

            <p className="mt-1 text-xs leading-5 text-slate-500">
              These settings will personalize your future learning
              sessions.
            </p>
          </div>

          <button
            type="button"
            className="rounded-xl bg-orange-500 px-5 py-3 text-sm font-bold text-white shadow-md shadow-orange-100 transition hover:bg-orange-600"
          >
            Save Preferences
          </button>
        </div>
      </section>
    </DashboardLayout>
  )
}

export default ProfilePage