export function changeTimestampToTime(value) {
    const date = new Date(value*1000).toLocaleDateString("en-US")
    const time = new Date(value*1000).toLocaleTimeString("en-US")
    return `${time} ${date}`
}