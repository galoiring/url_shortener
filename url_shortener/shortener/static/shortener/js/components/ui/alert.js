import React from "react";

export const Alert = ({
  children,
  variant = "default",
  className = "",
  ...props
}) => {
  const baseStyles =
    "relative w-full rounded-lg border p-4 [&>svg~*]:pl-7 [&>svg+div]:translate-y-[-3px] [&>svg]:absolute [&>svg]:left-4 [&>svg]:top-4 [&>svg]:text-foreground";

  const variants = {
    default: "bg-background text-foreground",
    destructive:
      "border-destructive/50 text-destructive dark:border-destructive [&>svg]:text-destructive",
  };

  return (
    <div
      role='alert'
      className={`${baseStyles} ${variants[variant]} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

export const AlertTitle = ({ className = "", ...props }) => (
  <h5
    className={`mb-1 font-medium leading-none tracking-tight ${className}`}
    {...props}
  />
);

export const AlertDescription = ({ className = "", ...props }) => (
  <div className={`text-sm [&_p]:leading-relaxed ${className}`} {...props} />
);
