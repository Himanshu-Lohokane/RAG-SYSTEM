"use client";

import Image from "next/image";
import Link from "next/link";
import { cn } from "@/lib/utils";

export type LogoVariant = "horizontal" | "vertical" | "icon";
export type LogoSize = "small" | "medium" | "large";

interface LogoProps {
  variant?: LogoVariant;
  size?: LogoSize;
  className?: string;
  clickable?: boolean;
  href?: string;
}

const sizeConfig = {
  small: {
    horizontal: { width: 140, height: 38 },
    vertical: { width: 80, height: 80 },
    icon: { width: 32, height: 32 }
  },
  medium: {
    horizontal: { width: 200, height: 54 },
    vertical: { width: 120, height: 120 },
    icon: { width: 48, height: 48 }
  },
  large: {
    horizontal: { width: 280, height: 75 },
    vertical: { width: 160, height: 160 },
    icon: { width: 64, height: 64 }
  }
};

const Logo = ({
  variant = "horizontal",
  size = "medium",
  className,
  clickable = true,
  href = "/dashboard"
}: LogoProps) => {
  const { width, height } = sizeConfig[size][variant];
  const logoSrc = `/logos/datatrack-${variant}.png`;

  const imageElement = (
    <Image
      src={logoSrc}
      alt="DataTrack KMRL - Document Management System"
      width={width}
      height={height}
      className={cn(
        "object-contain",
        clickable && "transition-opacity hover:opacity-80",
        className
      )}
      priority
      aria-label="DataTrack KMRL Logo"
    />
  );

  if (clickable) {
    return (
      <Link href={href} className="inline-block">
        {imageElement}
      </Link>
    );
  }

  return imageElement;
};

export { Logo };
