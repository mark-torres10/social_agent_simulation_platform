'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { 
  TrendingUp, 
  Shield, 
  Zap, 
  BarChart3, 
  Users, 
  Brain, 
  Target, 
  CheckCircle,
  ArrowRight,
  PlayCircle,
  Star,
  Building,
  Lightbulb,
  Globe
} from 'lucide-react'

const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.6 } }
}

const staggerContainer = {
  initial: {},
  animate: {
    transition: {
      staggerChildren: 0.1
    }
  }
}

const businessApplications = [
  {
    icon: TrendingUp,
    title: "Product Launch Risk Assessment",
    description: "Prevent costly failures before they happen. Test market reactions, messaging strategies, and predict viral adoption patterns.",
    roi: "$500K-$2M saved per prevented failure",
    color: "text-green-600"
  },
  {
    icon: Shield,
    title: "Crisis Communication Planning",
    description: "Model crisis responses, test PR strategies, and predict stakeholder reactions before implementation.",
    roi: "$1M-$50M in reputation protection",
    color: "text-red-600"
  },
  {
    icon: Zap,
    title: "Viral Marketing Optimization",
    description: "Predict which content will go viral, optimize timing, and model influencer collaboration strategies.",
    roi: "$200K-$1M improved campaign ROI",
    color: "text-yellow-600"
  },
  {
    icon: BarChart3,
    title: "Market Research Revolution",
    description: "Replace expensive focus groups with 100,000+ virtual consumers for instant, scalable insights.",
    roi: "80% reduction in research costs",
    color: "text-blue-600"
  },
  {
    icon: Users,
    title: "Competitive Intelligence",
    description: "Simulate competitor moves, test counter-strategies, and predict market share shifts.",
    roi: "$100K-$500K strategic advantage",
    color: "text-purple-600"
  },
  {
    icon: Brain,
    title: "Customer Behavior Analysis",
    description: "Model purchasing decisions, predict demographic responses, and optimize customer journeys.",
    roi: "15-25% improvement in conversion",
    color: "text-indigo-600"
  }
]

const testimonials = [
  {
    name: "Sarah Chen",
    role: "Chief Marketing Officer",
    company: "TechCorp",
    content: "Prophecy helped us avoid a $5M product launch disaster. The 76% accuracy prediction saved our company.",
    rating: 5
  },
  {
    name: "David Rodriguez",
    role: "VP of Strategy",
    company: "Global Brands Inc",
    content: "We've replaced our entire market research budget with Prophecy. 10x faster insights at 1/10th the cost.",
    rating: 5
  },
  {
    name: "Emily Thompson",
    role: "CEO",
    company: "Innovation Labs",
    content: "The viral marketing predictions are incredibly accurate. We've tripled our campaign success rate.",
    rating: 5
  }
]

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-neutral-900 via-neutral-800 to-neutral-900">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-neutral-900/80 backdrop-blur-sm border-b border-neutral-800 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-accent-500 rounded-lg flex items-center justify-center">
                <Brain className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-white">Prophecy</span>
            </div>
            <div className="hidden md:flex items-center space-x-8">
              <a href="#applications" className="text-neutral-300 hover:text-white transition-colors">Applications</a>
              <a href="#proof" className="text-neutral-300 hover:text-white transition-colors">Proof</a>
              <a href="#pricing" className="text-neutral-300 hover:text-white transition-colors">Pricing</a>
              <button className="btn-primary">Start Free Trial</button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-24 pb-16 lg:pt-32 lg:pb-24 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary-600/20 to-accent-600/20"></div>
        <motion.div 
          className="container mx-auto px-4 relative z-10"
          initial="initial"
          animate="animate"
          variants={staggerContainer}
        >
          <div className="text-center max-w-4xl mx-auto">
            <motion.div
              variants={fadeInUp}
              className="inline-flex items-center px-4 py-2 rounded-full bg-primary-500/10 border border-primary-500/20 text-primary-400 text-sm font-medium mb-6"
            >
              <Zap className="w-4 h-4 mr-2" />
              Transform Business Guesswork into Data-Driven Certainty
            </motion.div>
            
            <motion.h1 
              variants={fadeInUp}
              className="text-4xl md:text-6xl lg:text-7xl font-bold text-white mb-6"
            >
              Predict Reality
              <span className="text-gradient block">Before It Happens</span>
            </motion.h1>
            
            <motion.p 
              variants={fadeInUp}
              className="text-xl md:text-2xl text-neutral-300 mb-12 max-w-3xl mx-auto"
            >
              Simulate 1 million AI agents to predict product launches, prevent crises, and maximize profits. 
              <span className="text-primary-400 font-semibold"> 76% accuracy</span> vs real-world outcomes.
            </motion.p>
            
            <motion.div 
              variants={fadeInUp}
              className="flex flex-col sm:flex-row gap-4 justify-center items-center"
            >
              <button className="btn-primary text-lg px-8 py-4 group">
                Start Free Simulation
                <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
              </button>
              <button className="btn-outline text-lg px-8 py-4 group">
                <PlayCircle className="w-5 h-5 mr-2" />
                Watch 60s Demo
              </button>
            </motion.div>
            
            <motion.div 
              variants={fadeInUp}
              className="mt-12 flex items-center justify-center space-x-8 text-neutral-400"
            >
              <div className="flex items-center">
                <Users className="w-5 h-5 mr-2" />
                <span>1M+ AI Agents</span>
              </div>
              <div className="flex items-center">
                <Target className="w-5 h-5 mr-2" />
                <span>76% Accuracy</span>
              </div>
              <div className="flex items-center">
                <Zap className="w-5 h-5 mr-2" />
                <span>5-Minute Results</span>
              </div>
            </motion.div>
          </div>
        </motion.div>
      </section>

      {/* Business Applications Section */}
      <section id="applications" className="section bg-white">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="section-title text-neutral-900">
              15 Business-Critical Applications
            </h2>
            <p className="section-subtitle">
              Transform every major business decision with AI-powered simulations
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {businessApplications.map((app, index) => (
              <motion.div
                key={app.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="card p-6 group hover:shadow-glow transition-all duration-300"
              >
                <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${app.color} flex items-center justify-center mb-4`}>
                  <app.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-bold text-neutral-900 mb-3">{app.title}</h3>
                <p className="text-neutral-600 mb-4">{app.description}</p>
                <div className="bg-neutral-50 rounded-lg p-3">
                  <p className="text-sm font-semibold text-neutral-900">ROI: {app.roi}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Proof Section */}
      <section id="proof" className="section bg-gradient-to-r from-neutral-900 to-neutral-800">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="section-title text-white">
              Scientifically Proven Results
            </h2>
            <p className="section-subtitle text-neutral-300">
              Validated by Fortune 500 companies and leading research institutions
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-16">
            <div className="text-center">
              <div className="text-4xl font-bold text-primary-400 mb-2">76%</div>
              <div className="text-neutral-300">Accuracy vs Real World</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-accent-400 mb-2">88%</div>
              <div className="text-neutral-300">Accuracy for Major Effects</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-secondary-400 mb-2">1M+</div>
              <div className="text-neutral-300">Simultaneous Agents</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-success-400 mb-2">2000+</div>
              <div className="text-neutral-300">Successful Predictions</div>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={testimonial.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-white rounded-xl p-6 shadow-lg"
              >
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                  ))}
                </div>
                <p className="text-neutral-600 mb-4">"{testimonial.content}"</p>
                <div>
                  <div className="font-semibold text-neutral-900">{testimonial.name}</div>
                  <div className="text-sm text-neutral-500">{testimonial.role}, {testimonial.company}</div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="section bg-neutral-50">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="section-title text-neutral-900">
              Choose Your Competitive Advantage
            </h2>
            <p className="section-subtitle">
              Start free, scale with confidence
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="card p-8">
              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold text-neutral-900 mb-2">Explorer</h3>
                <div className="text-4xl font-bold text-neutral-900 mb-2">Free</div>
                <div className="text-neutral-600">Perfect for testing</div>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center">
                  <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                  <span>1,000 AI agents</span>
                </li>
                <li className="flex items-center">
                  <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                  <span>3 simulations/month</span>
                </li>
                <li className="flex items-center">
                  <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                  <span>Basic analytics</span>
                </li>
                <li className="flex items-center">
                  <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                  <span>Email support</span>
                </li>
              </ul>
              <button className="btn-outline w-full">Get Started</button>
            </div>
            
            <div className="card p-8 border-2 border-primary-500 relative">
              <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 bg-primary-500 text-white px-4 py-1 rounded-full text-sm font-medium">
                Most Popular
              </div>
              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold text-neutral-900 mb-2">Professional</h3>
                <div className="text-4xl font-bold text-neutral-900 mb-2">$497</div>
                <div className="text-neutral-600">per month</div>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center">
                  <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                  <span>100,000 AI agents</span>
                </li>
                <li className="flex items-center">
                  <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                  <span>Unlimited simulations</span>
                </li>
                <li className="flex items-center">
                  <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                  <span>Advanced analytics</span>
                </li>
                <li className="flex items-center">
                  <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                  <span>Priority support</span>
                </li>
                <li className="flex items-center">
                  <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                  <span>Custom scenarios</span>
                </li>
              </ul>
              <button className="btn-primary w-full">Start Free Trial</button>
            </div>
            
            <div className="card p-8">
              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold text-neutral-900 mb-2">Enterprise</h3>
                <div className="text-4xl font-bold text-neutral-900 mb-2">Custom</div>
                <div className="text-neutral-600">For large organizations</div>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center">
                  <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                  <span>1M+ AI agents</span>
                </li>
                <li className="flex items-center">
                  <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                  <span>Unlimited everything</span>
                </li>
                <li className="flex items-center">
                  <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                  <span>Full analytics suite</span>
                </li>
                <li className="flex items-center">
                  <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                  <span>Dedicated support</span>
                </li>
                <li className="flex items-center">
                  <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                  <span>API access</span>
                </li>
              </ul>
              <button className="btn-secondary w-full">Contact Sales</button>
            </div>
          </div>
          
          <div className="text-center mt-12">
            <p className="text-neutral-600 mb-4">
              30-day money-back guarantee
            </p>
            <p className="text-sm text-neutral-500">
              If Prophecy doesn't predict your business outcomes with 70%+ accuracy, 
              we'll refund every penny.
            </p>
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="section bg-gradient-to-r from-primary-600 to-accent-600">
        <div className="container">
          <div className="text-center">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Stop Guessing. Start Knowing.
            </h2>
            <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
              Join thousands of businesses that have transformed uncertainty into competitive advantage
            </p>
            <button className="btn-secondary text-lg px-8 py-4 group">
              Start Your Free Simulation
              <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-neutral-900 text-white py-12">
        <div className="container">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-accent-500 rounded-lg flex items-center justify-center">
                  <Brain className="w-5 h-5 text-white" />
                </div>
                <span className="text-xl font-bold">Prophecy</span>
              </div>
              <p className="text-neutral-400 text-sm">
                Transform business uncertainty into competitive advantage with AI-powered simulations.
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Applications</h4>
              <ul className="space-y-2 text-sm text-neutral-400">
                <li>Product Launch Testing</li>
                <li>Crisis Management</li>
                <li>Market Research</li>
                <li>Competitive Analysis</li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Resources</h4>
              <ul className="space-y-2 text-sm text-neutral-400">
                <li>Documentation</li>
                <li>Case Studies</li>
                <li>Blog</li>
                <li>Support</li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-neutral-400">
                <li>About</li>
                <li>Careers</li>
                <li>Privacy</li>
                <li>Terms</li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-neutral-800 mt-8 pt-8 text-center text-sm text-neutral-400">
            <p>&copy; 2024 Prophecy. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}