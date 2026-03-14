"""Gerenciamento de áudio 2D via QMediaPlayer (PyQt6)."""

from __future__ import annotations
from typing import Optional
from PyQt6.QtMultimedia import QMediaPlayer, QUrl


class AudioManager:
    def __init__(self) -> None:
        self.player = QMediaPlayer()

    def play(self, path: str, loop: bool = False, volume: int = 100) -> None:
        self.player.setSource(QUrl.fromLocalFile(path))
        self.player.setVolume(volume)
        if loop:
            self.player.setLoops(QMediaPlayer.Loops.Infinite)
        self.player.play()

    def stop(self) -> None:
        self.player.stop()

    def pause(self) -> None:
        self.player.pause()

    def set_volume(self, value: int) -> None:
        self.player.setVolume(value)

    def is_playing(self) -> bool:
        return self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState
