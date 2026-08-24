import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'

import LoginPage from '../pages/auth/LoginPage'
import RegisterPage from '../pages/auth/RegisterPage'
import LandingPage from '../pages/public/LandingPage'

// Student Pages
import DashboardPage from '../pages/student/DashboardPage'
import LearningPage from '../pages/student/LearningPage'
import LibraryPage from '../pages/student/LibraryPage'
import ProfilePage from '../pages/student/ProfilePage'
import ProgressPage from '../pages/student/ProgressPage'
import AccessibilityPage from '../pages/student/AccessibilityPage'
import AIVideoPage from '../pages/student/AIVideoPage'

// Teacher Pages
import TeacherDashboardPage from '../pages/teacher/TeacherDashboardPage'
import TeacherUploadPage from '../pages/teacher/TeacherUploadPage'
import TeacherContentPage from '../pages/teacher/TeacherContentPage'
import TeacherAnalyticsPage from '../pages/teacher/TeacherAnalyticsPage'
import TeacherProfilePage from '../pages/teacher/TeacherProfilePage'

function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Public */}
        <Route
          path="/"
          element={<LandingPage />}
        />

        <Route
          path="/login"
          element={<LoginPage />}
        />

        <Route
          path="/register"
          element={<RegisterPage />}
        />

        {/* ================= STUDENT ================= */}

        <Route
          path="/student"
          element={
            <Navigate
              to="/student/dashboard"
              replace
            />
          }
        />

        <Route
          path="/student/dashboard"
          element={<DashboardPage />}
        />

        <Route
          path="/student/learning"
          element={<LearningPage />}
        />

        <Route
          path="/student/library"
          element={<LibraryPage />}
        />

        <Route
          path="/student/progress"
          element={<ProgressPage />}
        />

        <Route
          path="/student/profile"
          element={<ProfilePage />}
        />

        <Route
          path="/student/accessibility"
          element={<AccessibilityPage />}
        />

        <Route
          path="/student/ai-video"
          element={<AIVideoPage />}
        />

        {/* ================= TEACHER ================= */}

        <Route
          path="/teacher"
          element={
            <Navigate
              to="/teacher/dashboard"
              replace
            />
          }
        />

        <Route
          path="/teacher/dashboard"
          element={<TeacherDashboardPage />}
        />

        <Route
          path="/teacher/upload"
          element={<TeacherUploadPage />}
        />

        <Route
          path="/teacher/content"
          element={<TeacherContentPage />}
        />

        <Route
          path="/teacher/analytics"
          element={<TeacherAnalyticsPage />}
        />

        <Route
          path="/teacher/profile"
          element={<TeacherProfilePage />}
        />

        {/* Fallback */}
        <Route
          path="*"
          element={
            <Navigate
              to="/"
              replace
            />
          }
        />

      </Routes>
    </BrowserRouter>
  )
}

export default AppRouter