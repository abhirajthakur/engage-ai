export default function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-border bg-card/80 backdrop-blur-sm">
      <div className="flex items-center justify-between px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary text-white font-bold text-sm">
            AI
          </div>
          <div>
            <h1 className="text-xl font-bold text-foreground">EngageAI</h1>
            <p className="text-xs text-muted-foreground">Video Engagement Analytics</p>
          </div>
        </div>
      </div>
    </header>
  );
}
