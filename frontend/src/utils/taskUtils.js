export const formatTimeAgo = (dateString) => {
    if (!dateString) return 'recently'

    const now = new Date()
    const dateStrUtc = dateString.endsWith('Z') || dateString.includes('+') ? dateString : dateString + 'Z'
    const date = new Date(dateStrUtc)

    if (isNaN(date.getTime())) return 'recently'

    const diffInMs = now - date
    const diffInSeconds = Math.floor(diffInMs / 1000)
    const diffInMinutes = Math.floor(diffInSeconds / 60)
    const diffInHours = Math.floor(diffInMinutes / 60)
    const diffInDays = Math.floor(diffInHours / 24)

    if (diffInSeconds < 60) return `Just now`
    if (diffInMinutes < 60) return `${diffInMinutes} minute${diffInMinutes > 1 ? 's' : ''} ago`
    if (diffInHours < 24) return `${diffInHours} hour${diffInHours > 1 ? 's' : ''} ago`

    return `${diffInDays} day${diffInDays > 1 ? 's' : ''} ago`
}

export const getDeadlineColorClass = (task) => {
    if (task.status === '1') return 'text-success'
    if (task.is_past_due || task.hours_until <= 24) return 'text-danger'
    if (task.hours_until <= 72) return 'text-orange'
    if (task.hours_until <= 168) return 'text-warning'
    return 'text-dark'
}

export const formatGroupOption = (group) => {
    const text = `${group.course_code} - ${group.course_name} (${group.group_name})`
    const MAX_LENGTH = 60
    if (text.length > MAX_LENGTH) {
        return text.substring(0, MAX_LENGTH - 3) + '...'
    }
    return text
}
