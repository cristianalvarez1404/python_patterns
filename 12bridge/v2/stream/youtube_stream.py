import logging
from dataclasses import dataclass
from stream.data import generate_id,Buffer

@dataclass
class YoutubeStreamingService:
  buffer: Buffer

  def start_stream(self) -> str:
    stream_reference = generate_id()
    logging.info(f"Starting Youtube stream with reference {stream_reference}.")
    return stream_reference

  def fill_buffer(self, stream_reference: str) -> None:
    buffer_data = self.buffer()
    logging.info(f"Received buffer data: {buffer_data}. Sending to Youtube with reference {stream_reference}")

  def stop_stream(self, stream_reference: str) -> None:
    logging.info(f"Closing Youtube stream with reference {stream_reference}")