import type { HTMLProps } from "react";
import type { Components } from "react-markdown";
export const MarkdownComponents: Components = {
  p: ({ children, ...props }: HTMLProps<HTMLParagraphElement>) => (
    <p className="my-1" {...props}>
      {children}
    </p>
  ),

  code: ({
    className,
    children,
    ...props
  }: HTMLProps<HTMLElement> & { inline?: boolean }) => {
    const isInline = props.inline;
    if (isInline) {
      return (
        <code className="bg-gray-100 px-1 py-0.5 rounded" {...props}>
          {children}
        </code>
      );
    }
    return (
      <pre className="bg-gray-100 p-3 rounded-lg overflow-x-auto">
        <code className={className} {...props}>
          {children}
        </code>
      </pre>
    );
  },

  a: ({ href, children, ...props }: HTMLProps<HTMLAnchorElement>) => (
    <a
      href={href}
      className="text-blue-500 hover:underline"
      target="_blank"
      rel="noopener noreferrer"
      {...props}
    >
      {children}
    </a>
  ),

  h1: ({ children, ...props }: HTMLProps<HTMLHeadingElement>) => (
    <h1 className="text-2xl font-bold my-4" {...props}>
      {children}
    </h1>
  ),

  h2: ({ children, ...props }: HTMLProps<HTMLHeadingElement>) => (
    <h2 className="text-xl font-bold my-3" {...props}>
      {children}
    </h2>
  ),

  h3: ({ children, ...props }: HTMLProps<HTMLHeadingElement>) => (
    <h3 className="text-lg font-bold my-2" {...props}>
      {children}
    </h3>
  ),

  ul: ({ children, ...props }: HTMLProps<HTMLUListElement>) => (
    <ul className="list-disc ml-4 my-2" {...props}>
      {children}
    </ul>
  ),
};
