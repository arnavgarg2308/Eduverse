export const supportedUploadTypes = [
  {
    id: 'pdf',
    label: 'PDF Document',
    description: 'Upload textbooks, notes or study material.',
    icon: '📄',
    extensions: '.pdf',
  },
  {
    id: 'ppt',
    label: 'PowerPoint',
    description: 'Upload presentation slides and lectures.',
    icon: '📊',
    extensions: '.ppt,.pptx',
  },
  {
    id: 'notes',
    label: 'Study Notes',
    description: 'Upload prepared notes and learning material.',
    icon: '📝',
    extensions: '.txt,.doc,.docx',
  },
]

export const uploadLanguages = [
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

export const uploadAccessibilityOptions = [
  {
    id: 'simplifiedNotes',
    title: 'Simplified Notes',
    description: 'Create easier-to-understand explanations.',
    icon: '📖',
    enabled: true,
  },
  {
    id: 'audioNarration',
    title: 'Audio Narration',
    description: 'Generate an accessible audio version.',
    icon: '🎧',
    enabled: true,
  },
  {
    id: 'videoLesson',
    title: 'AI Video Lesson',
    description: 'Convert the content into a visual lesson.',
    icon: '🎥',
    enabled: true,
  },
  {
    id: 'quizGeneration',
    title: 'AI Quiz',
    description: 'Generate questions to test understanding.',
    icon: '✓',
    enabled: true,
  },
  {
    id: 'accessibilityMode',
    title: 'Accessibility Adaptation',
    description:
      'Optimize content for diverse learning needs.',
    icon: '♿',
    enabled: true,
  },
]

export const uploadCategories = [
  'Computer Science',
  'Mathematics',
  'Physics',
  'Chemistry',
  'Biology',
  'Artificial Intelligence',
  'Other',
]

export const uploadDifficultyLevels = [
  'Beginner',
  'Intermediate',
  'Advanced',
]