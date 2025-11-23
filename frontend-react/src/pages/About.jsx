import { Sparkles, Music, Heart, Zap } from 'lucide-react'
import Card from '../components/UI/Card'

const About = () => {
  const features = [
    {
      icon: Sparkles,
      title: 'AI-Powered Generation',
      description: 'Advanced machine learning models create unique music tailored to your mood and preferences.',
    },
    {
      icon: Music,
      title: 'Spotify Integration',
      description: 'Discover and play millions of tracks with seamless Spotify recommendations.',
    },
    {
      icon: Heart,
      title: 'Mood-Based Creation',
      description: 'Express yourself through music that matches your emotional state perfectly.',
    },
    {
      icon: Zap,
      title: 'Instant Generation',
      description: 'Create professional-quality music in seconds with our optimized AI engine.',
    },
  ]

  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold text-gradient mb-4">About NexGenMusic</h1>
        <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
          The future of music creation is here. NexGenMusic combines cutting-edge AI technology
          with intuitive design to help you create, discover, and enjoy music like never before.
        </p>
      </div>

      {/* Features Grid */}
      <div className="grid md:grid-cols-2 gap-6 mb-12">
        {features.map((feature, index) => {
          const Icon = feature.icon
          return (
            <Card key={index} hoverTilt className="text-center">
              <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
                <Icon className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                {feature.description}
              </p>
            </Card>
          )
        })}
      </div>

      {/* Mission Statement */}
      <Card className="bg-gradient-to-br from-primary/10 to-secondary/10">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">Our Mission</h2>
        <p className="text-lg text-gray-700 dark:text-gray-300 mb-4">
          At NexGenMusic, we believe that everyone should have the power to create and enjoy music
          that resonates with their emotions. Our mission is to democratize music creation through
          innovative AI technology, making it accessible, intuitive, and fun for everyone.
        </p>
        <p className="text-lg text-gray-700 dark:text-gray-300">
          Whether you're a professional musician, a casual listener, or someone exploring music
          for the first time, NexGenMusic provides the tools and inspiration you need to express
          yourself through sound.
        </p>
      </Card>

      {/* Contact Section */}
      <div className="mt-12 text-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Get in Touch</h2>
        <p className="text-gray-600 dark:text-gray-400 mb-6">
          Have questions or feedback? We'd love to hear from you!
        </p>
        <div className="flex justify-center gap-4">
          <a
            href="mailto:support@nexgenmusic.com"
            className="px-6 py-3 bg-gradient-to-r from-primary to-secondary text-white rounded-xl font-medium hover:shadow-glow transition-all"
          >
            Contact Support
          </a>
          <a
            href="https://github.com/nexgenmusic"
            target="_blank"
            rel="noopener noreferrer"
            className="px-6 py-3 bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white rounded-xl font-medium hover:bg-gray-300 dark:hover:bg-gray-600 transition-all"
          >
            View on GitHub
          </a>
        </div>
      </div>
    </div>
  )
}

export default About
