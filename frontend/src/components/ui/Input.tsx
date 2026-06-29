import { type InputHTMLAttributes, type TextareaHTMLAttributes } from 'react'
import { cn } from '@/lib/utils'

export function Input({ className, ...props }: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      className={cn(
        'terminal w-full rounded-md border border-border bg-surface px-3 py-1.5 text-sm text-foreground outline-none placeholder:text-muted focus:border-accent',
        className,
      )}
      {...props}
    />
  )
}

export function Textarea({ className, ...props }: TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <textarea
      className={cn(
        'terminal w-full rounded-md border border-border bg-surface px-3 py-1.5 text-sm text-foreground outline-none placeholder:text-muted focus:border-accent',
        className,
      )}
      {...props}
    />
  )
}
