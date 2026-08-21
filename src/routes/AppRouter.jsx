import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'

// ==============================
// Public Pages
// ==============================
import LandingPage from '../pages/public/LandingPage'

// ==============================
// Authentication
// ==============================
import LoginPage from '../pages/auth/LoginPage'
import RegisterPage from '../pages/auth/RegisterPage'

// ==============================
// Student Pages
// ==============================
import DashboardPage from '../pages/student/DashboardPage'
import LibraryPage from '../pages/student/LibraryPage'
import LearningPage from '../pages/student/LearningPage'
import ProgressPage from '../pages/student/ProgressPage'
import ProfilePage from '../pages/student/ProfilePage'
import AccessibilityPage from '../pages/student/AccessibilityPage'

// ==============================
// Teacher Pages — EduVerse
// ==============================
import TeacherDashboardPage from '../pages/teacher/TeacherDashboardPage'
import TeacherUploadPage from '../pages/teacher/TeacherUploadPage'
import TeacherContentPage from '../pages/teacher/TeacherContentPage'
import TeacherAnalyticsPage from '../pages/teacher/TeacherAnalyticsPage'
import TeacherProfilePage from '../pages/teacher/TeacherProfilePage'

function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        {/* ==================================================
            EDVERSE — PUBLIC
        ================================================== */}

        <Route
          path="/"
          element={<LandingPage />}
        />

        {/* ==================================================
            AUTHENTICATION
        ================================================== */}

        <Route
          path="/login"
          element={<LoginPage />}
        />

        <Route
          path="/register"
          element={<RegisterPage />}
        />

        {/* ==================================================
            EDVERSE — STUDENT
        ================================================== */}

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
          path="/student/library"
          element={<LibraryPage />}
        />

        <Route
          path="/student/learning/:courseId"
          element={<LearningPage />}
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

        {/* ==================================================
            EDVERSE — TEACHER
        ================================================== */}

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

        {/* ==================================================
            UNKNOWN ROUTE
        ================================================== */}

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