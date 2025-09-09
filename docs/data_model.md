# Data Model

This project uses a small set of dataclasses to describe YouTube content and
how it is processed.  All classes live in
`src/youtube_scanner/models.py` and share a common design:

* **JSON serialisation** – the `to_json()` and `from_json()` helpers convert
  instances to and from JSON strings using the standard library.
* **CSV serialisation** – the `csv_headers()` and `to_csv_row()` helpers make
  it easy to write collections of instances to CSV files.  The
  corresponding `from_csv_row()` constructors reverse the process.

## `VideoMetadata`

Describes basic information about a video.

| field | type | description |
| --- | --- | --- |
| `video_id` | `str` | Unique identifier for the video. |
| `title` | `str` | Video title. |
| `description` | `str` | Description text. |
| `publish_date` | `datetime` \| `None` | Time the video was published. |
| `view_count` | `int` \| `None` | Number of views. |
| `like_count` | `int` \| `None` | Number of likes. |
| `comment_count` | `int` \| `None` | Number of comments. |
| `duration` | `int` \| `None` | Length of the video in seconds. |
| `is_short` | `bool` | Flag indicating if this video is a YouTube Short. |

## `ShortMapping`

Represents a link between a Short and its corresponding long-form video.

| field | type | description |
| --- | --- | --- |
| `short_video_id` | `str` | Identifier of the short video. |
| `full_video_id` | `str` \| `None` | Identifier of the long-form video. |
| `relation_source` | `str` \| `None` | How the mapping was determined. |

## `ChannelConfig`

Defines configuration values for scanning a YouTube channel.

| field | type | description |
| --- | --- | --- |
| `channel_id` | `str` | The channel's unique identifier. |
| `name` | `str` | Human readable channel name. |
| `category` | `str` \| `None` | Optional categorisation for the channel. |
| `short_view_threshold` | `int` | Minimum views for a Short to be included. |
| `top_n_shorts` | `int` | Number of top Shorts to retain per channel. |
