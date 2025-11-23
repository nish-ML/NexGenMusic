import { useEffect } from 'react'

export const useKeyboardShortcuts = (shortcuts) => {
  useEffect(() => {
    const handleKeyDown = (event) => {
      // Don't trigger shortcuts when typing in inputs
      if (
        event.target.tagName === 'INPUT' ||
        event.target.tagName === 'TEXTAREA' ||
        event.target.isContentEditable
      ) {
        return
      }

      const key = event.key.toLowerCase()
      const ctrl = event.ctrlKey || event.metaKey
      const shift = event.shiftKey
      const alt = event.altKey

      Object.entries(shortcuts).forEach(([shortcut, callback]) => {
        const parts = shortcut.toLowerCase().split('+')
        const shortcutKey = parts[parts.length - 1]
        const needsCtrl = parts.includes('ctrl') || parts.includes('cmd')
        const needsShift = parts.includes('shift')
        const needsAlt = parts.includes('alt')

        if (
          key === shortcutKey &&
          ctrl === needsCtrl &&
          shift === needsShift &&
          alt === needsAlt
        ) {
          event.preventDefault()
          callback(event)
        }
      })
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [shortcuts])
}

// Usage example:
// useKeyboardShortcuts({
//   'g': () => handleGenerate(),
//   ' ': () => togglePlay(),
//   'ctrl+s': () => handleSave(),
// })
