export const teacherProfile = {
  name: 'Dr. Ananya Sharma',
  email: 'ananya@edumorph.ai',
  role: 'Teacher',
  institution: 'EduMorph Learning',
  department: 'Computer Science',
  experience: '6 Years',
}

export const teacherStats = {
  totalContent: 24,
  publishedContent: 18,
  processingContent: 3,
  totalStudents: 186,
  averageEngagement: 78,
}

export const uploadedContent = [
  {
    id: 'content-001',
    title: 'Data Structures & Algorithms',
    subject: 'Computer Science',
    type: 'PDF',
    size: '4.8 MB',
    uploadedOn: 'Today',
    status: 'Published',
    students: 64,
    languages: 4,
    progress: 100,
  },
  {
    id: 'content-002',
    title: 'Database Management Systems',
    subject: 'Computer Science',
    type: 'PPT',
    size: '8.2 MB',
    uploadedOn: 'Yesterday',
    status: 'Processing',
    students: 42,
    languages: 2,
    progress: 68,
  },
  {
    id: 'content-003',
    title: 'Operating Systems Fundamentals',
    subject: 'Computer Science',
    type: 'PDF',
    size: '6.1 MB',
    uploadedOn: '2 days ago',
    status: 'Published',
    students: 51,
    languages: 3,
    progress: 100,
  },
  {
    id: 'content-004',
    title: 'Computer Networks',
    subject: 'Computer Science',
    type: 'Notes',
    size: '2.4 MB',
    uploadedOn: '4 days ago',
    status: 'Draft',
    students: 29,
    languages: 1,
    progress: 25,
  },
  {
    id: 'content-005',
    title: 'Artificial Intelligence Basics',
    subject: 'Artificial Intelligence',
    type: 'PDF',
    size: '5.7 MB',
    uploadedOn: '1 week ago',
    status: 'Published',
    students: 37,
    languages: 5,
    progress: 100,
  },
]

export const processingQueue = [
  {
    id: 'process-001',
    title: 'Database Management Systems',
    type: 'PPT',
    progress: 68,
    currentStep: 'Generating multilingual content',
    estimatedTime: '2 min remaining',
  },
  {
    id: 'process-002',
    title: 'Computer Networks',
    type: 'PDF',
    progress: 42,
    currentStep: 'Creating accessible notes',
    estimatedTime: '4 min remaining',
  },
  {
    id: 'process-003',
    title: 'Operating Systems Quiz',
    type: 'PDF',
    progress: 84,
    currentStep: 'Generating assessment',
    estimatedTime: '1 min remaining',
  },
]

export const studentEngagement = [
  {
    day: 'Mon',
    students: 82,
  },
  {
    day: 'Tue',
    students: 96,
  },
  {
    day: 'Wed',
    students: 74,
  },
  {
    day: 'Thu',
    students: 118,
  },
  {
    day: 'Fri',
    students: 104,
  },
  {
    day: 'Sat',
    students: 132,
  },
  {
    day: 'Sun',
    students: 91,
  },
]

export const teacherRecentActivity = [
  {
    id: 'teacher-activity-001',
    title: 'Uploaded Data Structures PDF',
    type: 'Content',
    time: 'Today',
    icon: '📄',
  },
  {
    id: 'teacher-activity-002',
    title: 'Published AI Basics lesson',
    type: 'Published',
    time: 'Yesterday',
    icon: '✓',
  },
  {
    id: 'teacher-activity-003',
    title: 'Database content processing started',
    type: 'AI Processing',
    time: 'Yesterday',
    icon: '✦',
  },
  {
    id: 'teacher-activity-004',
    title: 'Viewed student engagement',
    type: 'Analytics',
    time: '2 days ago',
    icon: '📊',
  },
]

export const contentTypes = [
  'All Content',
  'PDF',
  'PPT',
  'Notes',
]

export const contentStatuses = [
  'All Status',
  'Published',
  'Processing',
  'Draft',
]