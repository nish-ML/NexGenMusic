// Analytics event tracking placeholders
// Replace with your analytics provider (Google Analytics, Mixpanel, etc.)

export const trackEvent = (eventName, properties = {}) => {
  if (import.meta.env.DEV) {
    console.log('📊 Analytics Event:', eventName, properties)
  }

  // Example: Google Analytics
  // if (window.gtag) {
  //   window.gtag('event', eventName, properties)
  // }

  // Example: Mixpanel
  // if (window.mixpanel) {
  //   window.mixpanel.track(eventName, properties)
  // }
}

export const trackPageView = (pageName) => {
  trackEvent('page_view', { page: pageName })
}

export const trackMusicGeneration = (mood, tempo, genre) => {
  trackEvent('music_generated', { mood, tempo, genre })
}

export const trackSpotifyClick = (trackId, trackName) => {
  trackEvent('spotify_track_clicked', { trackId, trackName })
}

export const trackDownload = (trackId, trackName) => {
  trackEvent('track_downloaded', { trackId, trackName })
}

export const trackThemeChange = (theme) => {
  trackEvent('theme_changed', { theme })
}
