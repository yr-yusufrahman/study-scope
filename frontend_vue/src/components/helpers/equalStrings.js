export default function equalStrings(str1, str2) {
    return str1.replace(/\s/g, "") === str2.replace(/\s/g, "")
}

