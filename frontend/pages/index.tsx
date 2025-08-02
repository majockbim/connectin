import { useState } from 'react'
import axios from 'axios'

export default function Home() {
  const [learnerUrl, setLearnerUrl] = useState('')
  const [mentorUrl, setMentorUrl] = useState('')
  const [questions, setQuestions] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setQuestions('')

    try {
      const response = await axios.post('http://localhost:8000/generate', {
        learner_url: learnerUrl,
        mentor_url: mentorUrl
      })
      
      setQuestions(response.data.questions)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An error occurred while generating questions')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8 text-gray-900">
          LinkedIn Coffee Chat Question Generator
        </h1>
        
        <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-md mb-8">
          <div className="mb-4">
            <label htmlFor="learner" className="block text-sm font-medium text-gray-700 mb-2">
              Learner LinkedIn URL
            </label>
            <input
              type="url"
              id="learner"
              value={learnerUrl}
              onChange={(e) => setLearnerUrl(e.target.value)}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="https://linkedin.com/in/learner-profile"
            />
          </div>
          
          <div className="mb-6">
            <label htmlFor="mentor" className="block text-sm font-medium text-gray-700 mb-2">
              Mentor LinkedIn URL
            </label>
            <input
              type="url"
              id="mentor"
              value={mentorUrl}
              onChange={(e) => setMentorUrl(e.target.value)}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="https://linkedin.com/in/mentor-profile"
            />
          </div>
          
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-blue-300 disabled:cursor-not-allowed"
          >
            {loading ? 'Generating Questions...' : 'Generate Questions'}
          </button>
        </form>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-8">
            {error}
          </div>
        )}

        {questions && (
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4 text-gray-900">Generated Questions</h2>
            <div className="whitespace-pre-wrap text-gray-700">
              {questions}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}