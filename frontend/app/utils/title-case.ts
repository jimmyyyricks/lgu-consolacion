const lowercaseWords = new Set([
  'a',
  'an',
  'and',
  'as',
  'at',
  'but',
  'by',
  'for',
  'from',
  'in',
  'nor',
  'of',
  'on',
  'or',
  'the',
  'to',
  'with'
])

export function titleCaseLabel(value: string): string {
  const words = value.replaceAll('_', ' ').trim().toLowerCase().split(/\s+/)

  return words.map((word, index) => {
    if (index > 0 && index < words.length - 1 && lowercaseWords.has(word)) {
      return word
    }

    return word.charAt(0).toUpperCase() + word.slice(1)
  }).join(' ')
}
