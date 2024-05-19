export default function autoResize(textarea) {
    textarea.style.height = 'auto'; // Reset height to auto to calculate the actual height needed
    textarea.style.height = textarea.scrollHeight + 'px'; // Set the height to the scrollHeight
    if (textarea.scrollHeight < textarea.clientHeight) {
        textarea.style.height = textarea.clientHeight + 'px'; // Set the height to the current client height if it's smaller than scroll height
    }
}