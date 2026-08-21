export const profileData = {
  name: 'Rahul Sharma',
  email: 'rahul@example.com',
  role: 'Student',
  institution: 'EduMorph Learning',
  course: 'B.Tech Computer Science',
  year: '2nd Year',
  avatar: null,
}

export const learningPreferences = {
  language: 'Hindi',
  learningMode: 'Visual + Audio',
  contentDifficulty: 'Adaptive',
}

export const supportedLearningLanguages = [
  {
    name: 'English',
    nativeName: 'English',
    code: 'EN',
  },
  {
    name: 'Hindi',
    nativeName: 'हिन्दी',
    code: 'HI',
  },
  {
    name: 'Bengali',
    nativeName: 'বাংলা',
    code: 'BN',
  },
  {
    name: 'Tamil',
    nativeName: 'தமிழ்',
    code: 'TA',
  },
  {
    name: 'Telugu',
    nativeName: 'తెలుగు',
    code: 'TE',
  },
  {
    name: 'Marathi',
    nativeName: 'मराठी',
    code: 'MR',
  },
]

export const learningModes = [
  {
    id: 'visual',
    label: 'Visual',
    description: 'Learn through videos, diagrams and visual explanations.',
    icon: '◉',
  },
  {
    id: 'audio',
    label: 'Audio',
    description: 'Learn through narration and audio explanations.',
    icon: '♫',
  },
  {
    id: 'reading',
    label: 'Reading',
    description: 'Learn through notes, summaries and written explanations.',
    icon: '▤',
  },
  {
    id: 'mixed',
    label: 'Visual + Audio',
    description: 'Combine visual lessons with audio narration.',
    icon: '✦',
  },
]

export const accessibilityPreferences = [
  {
    id: 'dyslexiaFriendly',
    title: 'Dyslexia Friendly',
    description: 'Improve readability, spacing and text presentation.',
    icon: 'Aa',
    enabled: false,
  },
  {
    id: 'focusMode',
    title: 'Focus Mode',
    description: 'Reduce distractions while studying.',
    icon: '◎',
    enabled: false,
  },
  {
    id: 'highContrast',
    title: 'High Contrast',
    description: 'Increase contrast for better visual clarity.',
    icon: '◐',
    enabled: false,
  },
  {
    id: 'largerText',
    title: 'Larger Text',
    description: 'Increase the size of educational content.',
    icon: 'A+',
    enabled: false,
  },
  {
    id: 'audioNarration',
    title: 'Audio Narration',
    description: 'Listen to educational content while reading.',
    icon: '♫',
    enabled: true,
  },
]

export const notificationPreferences = [
  {
    id: 'learningReminder',
    title: 'Learning Reminders',
    description: 'Get reminders to continue your learning.',
    enabled: true,
  },
  {
    id: 'courseUpdates',
    title: 'Course Updates',
    description: 'Receive updates about your enrolled content.',
    enabled: true,
  },
  {
    id: 'achievementAlerts',
    title: 'Achievement Alerts',
    description: 'Get notified when you unlock a milestone.',
    enabled: true,
  },
]