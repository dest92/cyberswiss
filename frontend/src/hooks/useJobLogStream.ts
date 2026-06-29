import { useEffect, useRef, useState } from 'react'
import { apiBaseUrl } from '@/lib/api'

export function useJobLogStream(jobId: string | null) {
  const [lines, setLines] = useState<string[]>([])
  const [connected, setConnected] = useState(false)
  const socketRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    if (!jobId) return

    setLines([])
    const wsUrl = `${apiBaseUrl.replace(/^http/, 'ws')}/ws/jobs/${jobId}/logs`
    const socket = new WebSocket(wsUrl)
    socketRef.current = socket

    socket.onopen = () => setConnected(true)
    socket.onmessage = (event) => {
      setLines((prev) => [...prev, event.data as string])
    }
    socket.onclose = () => setConnected(false)
    socket.onerror = () => setConnected(false)

    return () => {
      socket.close()
      socketRef.current = null
    }
  }, [jobId])

  return { lines, connected }
}
