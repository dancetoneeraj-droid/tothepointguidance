export const STORAGE_VERSION = 1;
export const ACTIVE_STUDENT_KEY = "tothepoint:activeStudentId";
export const studentDataKey = (studentId: string) =>
  `tothepoint:v${STORAGE_VERSION}:student:${studentId}`;
export const GUEST_STUDENT_ID = "guest";
