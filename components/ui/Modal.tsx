"use client";

import { useEffect } from "react";
import { X } from "lucide-react";
import { Button } from "./Button";

interface ModalProps {
  open: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

export function Modal({ open, onClose, title, children, footer }: ModalProps) {
  useEffect(() => {
    if (!open) return;
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", handler);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", handler);
      document.body.style.overflow = "";
    };
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-4">
      <div
        className="absolute inset-0 bg-black/70 backdrop-blur-sm"
        onClick={onClose}
        aria-hidden
      />
      <div
        role="dialog"
        aria-modal
        aria-labelledby="modal-title"
        className="relative w-full max-w-md rounded-2xl border border-border bg-surface-elevated p-6 shadow-2xl animate-in"
      >
        <div className="flex items-start justify-between gap-4 mb-4">
          <h2 id="modal-title" className="text-lg font-semibold text-foreground">
            {title}
          </h2>
          <button
            onClick={onClose}
            className="rounded-lg p-1 text-muted hover:text-foreground hover:bg-surface-hover transition-colors"
            aria-label="Close"
          >
            <X className="h-5 w-5" />
          </button>
        </div>
        <div className="text-muted text-sm leading-relaxed">{children}</div>
        {footer ? <div className="mt-6 flex flex-col sm:flex-row gap-3">{footer}</div> : null}
      </div>
    </div>
  );
}

interface OverrideModalProps {
  open: boolean;
  onGoBack: () => void;
  onOverride: () => void;
  previousDay: number;
}

export function OverrideModal({
  open,
  onGoBack,
  onOverride,
  previousDay,
}: OverrideModalProps) {
  return (
    <Modal
      open={open}
      onClose={onGoBack}
      title="Incomplete previous day"
      footer={
        <>
          <Button variant="secondary" className="flex-1" onClick={onGoBack}>
            Go Back & Complete
          </Button>
          <Button variant="danger" className="flex-1" onClick={onOverride}>
            Override & Continue
          </Button>
        </>
      }
    >
      <p>
        You have incomplete tasks from Day {previousDay}. Are you sure you want
        to continue without finishing them?
      </p>
    </Modal>
  );
}

