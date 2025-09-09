Enterprise-Grade Plan for Parsing YouTube Shorts & Long-Form Video Links
Key Objectives & Requirements

Use Open & Public Tools: The solution will utilize public APIs (e.g. YouTube Data API) and open-source libraries (such as youtube-dl/yt-dlp or similar) to gather data, avoiding proprietary systems. This ensures transparency and reproducibility.

Scheduled Monthly Scans: Implement a scheduler (e.g. a cron job or cloud function) to scan each target YouTube channel once per month. This keeps the data up-to-date by capturing new Shorts or updated view counts on a regular interval.

Comprehensive Metadata Collection: For each video (both Shorts and any identified full-length originals), collect all available metadata – including title, description, publish date, view count, like count, comments (for linking info), and even transcripts/captions when available. Capturing the transcript is important for search and verification, and can be done via YouTube’s caption API or open libraries
stackoverflow.com
.

Robust Short-to-Long Mapping: Use best-practice strategies to reliably find if a Short has a corresponding long-form video. In particular, examine the Short’s description (“About” section) for any mention or URL of a longer video, and scan comments (especially the pinned comment by the channel owner if present) for a link to the full video
reddit.com
reddit.com
. If no direct link is provided, apply other methods (described below) to match Shorts to potential original videos.

Focus on Top Shorts (≥50K views or Top 20): Prioritize high-engagement content. For each channel, the system will target Shorts with over 50,000 views, ensuring popular clips are analyzed. Additionally, even if a channel has few or no Shorts above that threshold, include the top ~20 Shorts by view count for that channel to capture its most significant short-form content. This balances thoroughness with efficiency, focusing on the most relevant videos by popularity.

1. Channel Scanning and Video Retrieval

Task 1.1: Fetch Channel Uploads – For each YouTube channel in the list, retrieve the full list of uploaded videos. This can be done via the YouTube Data API’s channel resources to get the channel’s “uploads” playlist ID
developers.google.com
, then using the PlaylistItems API to list all videos. (Alternatively, an open-source tool like yt-dlp can fetch all video IDs from a channel’s uploads.) Ensure the system can handle channels with large numbers of videos by using pagination (API page tokens or iterative fetch in yt-dlp).

Task 1.2: Identify Shorts vs. Long-Form – Among the retrieved videos, determine which ones are YouTube Shorts. YouTube doesn’t explicitly label “Shorts” via API, but we can infer it by video duration. For each video, check the contentDetails.duration (via API) or use metadata from yt-dlp to get length; mark videos of 60 seconds or less as potential Shorts. (Most Shorts are vertical videos ≤60s.) It's also wise to verify using other cues: Shorts often have a video URL format using /shorts/ on YouTube, but since we have the video IDs, duration is a reliable indicator. Separate the list of videos into “Shorts” and “standard videos” for the next steps.

Task 1.3: Gather Basic Metadata – As we fetch the videos, store key metadata for each: title, video ID, publish date, and view count (from the videos.list API or scraping the page as needed). This initial metadata will be used to filter by popularity and to assist in matching Shorts to full videos. Ensure to also record the channel name and a predefined Category (as given in the table, e.g. Finance, Education) for each video for reporting purposes.

2. Filtering High-View Shorts (Threshold & Top 20)

Task 2.1: Apply View Count Filter – From the list of Shorts per channel, filter those that have ≥50,000 views. These Shorts are high-engagement clips likely worth linking to long-form content. Using the stored view counts, create a subset list of all Shorts above the threshold for each channel.

Task 2.2: Select Top 20 Shorts – In addition to the threshold filter, determine the top 20 Shorts by view count for each channel. Sort all Shorts by views in descending order and take the top 20 entries. This ensures that even if some top Shorts have slightly less than 50k views (for smaller channels), they are still included for analysis. If a channel already has 20 or more Shorts above 50k, then this “top 20” will naturally be a subset of those. If a channel has fewer than 20 Shorts total, just take all of them (the filter will then just be those above 50k, if any). The goal is to have a comprehensive yet focused list of Shorts per channel to investigate.

Task 2.3: Prepare List of Target Shorts – Merge the results of 2.1 and 2.2 for each channel. This yields the final set of target Shorts to process (ensuring no duplicates). For each target Short, we will next attempt to find a corresponding full-length video (if it exists). Each target Short entry at this stage includes its channel, title, view count, and video ID.

3. Mapping Shorts to Full-Length Videos

For each Short in the target list, perform a series of checks to find if it’s derived from or related to a longer video on the same channel (or occasionally another channel, though likely the same channel):

(3a) Check Short Description for Links: Retrieve the Short’s description text (using the API’s snippet.description or via scraping the video page HTML). Scan the description for any YouTube URL or mention of a full video. Creators often include phrases like “Full video: https://youtube.com/watch?v=…”. If a hyperlink to another YouTube video is present, extract that URL/ID as the potential full-length video. Also look for non-URL references such as a title or unique phrase that could be the long video’s title.

(3b) Check Pinned Comment: Using the YouTube comments API (commentThreads.list) or an HTML fetch of the comments section, retrieve the pinned comment on the Short (if one exists). Focus on comments by the channel owner (the creator) as these often contain extra info. Many creators pin their own comment with a link to the full video
reddit.com
. If the pinned comment (or any top comment by the creator) contains a YouTube link or directions (e.g. “Watch the full interview here: [link]”), capture that link. (The YouTube API can flag if a comment is pinned via the snippet.topLevelComment.snippet.textDisplay along with a snippet.isPinned true flag in the comment thread resource.)

(3c) Cross-Search by Title/Keywords: If neither the description nor comments yielded a direct link, use the Short’s title or key phrases to search for a matching long-form video. For example, take a distinctive part of the Short’s title (or an important keyword, such as a guest’s name in an interview) and search within the same channel’s video titles for a match. The YouTube Data API’s search endpoint can be used with channelId and a query string. Alternatively, use the channel’s uploads list to find titles that closely match or encompass the Short’s title/topic. (For instance, if a Kurzgesagt short is titled “Black Holes in 1 Minute”, the channel may have a full video titled “The Truth about Black Holes” – searching for “Black Holes” on that channel could surface it.)

(3d) Transcript Snippet Matching: As a robust fallback, leverage transcripts. Since we are collecting transcripts for all videos, we can take the transcript text of the Short (if available) and attempt to find that exact text within the transcripts of longer videos on the channel. A substring match could indicate the Short’s dialogue comes from a particular timestamp in a full video. For example, if a short contains a quote or fact, searching the full videos’ subtitles for a few words from that quote can pinpoint the source video
stackoverflow.com
. This method can reliably match Shorts to their source even when titles/descriptions don’t make it obvious, as long as captions exist (either creator-provided or auto-generated). It is more computationally intensive, so it should be used after simpler methods above.

(3e) Record Mapped Pair: If any of the above steps identify a likely full-length video for the Short, record the mapping. We should store the full video’s ID/link and title alongside the Short’s info. In cases where multiple Shorts map to the same full video (e.g. a podcast channel might cut several Shorts from one long interview), we will associate all those Shorts with that one full video entry. If a Short cannot be mapped confidently to any longer video (e.g. truly standalone Shorts or no clues found), mark it as “No full video found” or leave that field blank in the table.

4. Data Enrichment and Metadata Gathering

To meet the requirement of all available metadata, the system will gather detailed info for each identified Short and each matched full-length video:

Video Details: Using YouTube Data API’s videos.list for each video ID (Short or full), retrieve comprehensive details – including view count, like count, comment count, duration, upload date, tags, etc. This ensures our records are rich and can be filtered or analyzed later as needed.

Transcript Retrieval: For each video, attempt to get the transcript (closed captions). If the video has an official transcript or subtitles, use YouTube’s caption download URL (e.g. the timedtext XML endpoint) to fetch it
stackoverflow.com
. If only auto-generated captions exist (which the timedtext URL might not return without additional parameters), consider using an open-source library like youtube-transcript-api
stackoverflow.com
 that can fetch auto-generated transcripts. Save the transcript text for searchability and verification purposes. Note: transcripts of long videos can be large; ensure the storage and processing can handle this volume (possibly store just the text or a compressed form).

Category and Channel Info: Retain the channel name and the predefined Category (e.g. Education, Finance) for each entry as given in the input list. This categorization is likely provided manually, so we’ll use the given mapping in the final table. (If needed, the system could allow adding new channels with their category as configuration.)

All this metadata and text will be stored in a structured format (such as a database or JSON files) to feed into the final reporting table and for any future analysis.

5. Populating the Results Table

With the mapping information and metadata collected, we will produce the table of Shorts and their related full-length videos. The format (as drafted in the prompt) has columns: YouTube Channel | Category | Video (full-length) | Short | Short 2 | Short 3 …. The plan to populate this is:

Group by Full Video: For each channel, take each identified full-length video (that had one or more Shorts linked) as a separate row in the table. List the Full Video’s title or URL in the “Video” column. If a full video has multiple Shorts derived from it (as found in step 3e), list that full video once, and then fill the “Short”, “Short 2”, etc. columns with the URLs (or IDs) of each Short linked to it. For example, in the draft table Dwarkesh Patel has one full video with several Shorts listed in the row – our process will replicate that grouping.

Singles and Non-matches: If a Short is found to correspond to a full video that itself isn’t in our list (say the short is from another channel’s content or a collaboration), we can still list the Short and put the identified full video URL. However, since our focus is the given channels, most full videos should be from the same channel. If a Short does not have any matching full video (standalone content), we may omit it from the table or include it with the “Video” column blank to indicate no longer form counterpart. (For clarity, probably better to exclude those from the final enterprise table, as it focuses on mappings.)

Include View Metrics (Optional): An enterprise-grade report might also include additional columns or notes, such as the view counts of each Short (and maybe the full video) to give context. The prompt’s table didn’t show view counts, but since we have them, we might include them in a separate report or use them to prioritize which entries to show if the table needs to be limited in size.

Verification: Before finalizing an entry, optionally verify the Short-to-Video link by cross-checking that the full video’s content indeed covers the Short’s content (using the transcript match or manual spot-check at the timestamp). This ensures the table is accurate for enterprise use.

Once compiled, this table provides a clear mapping of Shorts to their longer videos for each channel, enabling quick identification of related content.

6. Continuous Monitoring & Updates

After the initial population of the table, the system will run on a monthly schedule to update and expand the data:

Monthly Delta Scan: Each month, for each channel, fetch the latest uploads (incremental since last scan). Identify any new Shorts posted or any that have newly crossed the 50k view threshold. Also update view counts of existing entries if needed (to possibly bring new Shorts into the top 20).

Update Mapping: For any new Shorts found, repeat the mapping process (section 3) to find their full video links. If new full-length videos are discovered (e.g., the channel posted a new long video and also Shorts for it), add new rows to the table. If new Shorts map to an existing full video in our table, simply append those Shorts into the respective row (e.g., Short 6, Short 7 columns, etc., or as a new line if the table is one Short per line for that channel in some implementations).

Re-scan Unresolved Shorts: If in previous runs some Shorts had "no match", consider re-checking them in case the creator later added a pinned comment or updated the description with the full video link (this can happen).

Quality Control: Log any failures or ambiguities (for example, if two possible full videos could be matches for a Short, flag for manual review). Enterprise-grade parsing should include robust logging and possibly alerting if the linking strategy fails for a popular short, so that analysts can manually intervene if necessary.

Data Storage & Access: Store the accumulated results in a database or spreadsheet. Each monthly run appends new findings. Ensure old data is not lost – maintain history or at least the latest state of the mapping. This database can then be queried or exported to refresh the master table.

Open Source Tools for Maintenance: Use open-source scheduling and orchestration tools (e.g. Apache Airflow for workflows or GitHub Actions if the project is on GitHub) to automate the monthly run. All code and configuration for the system will be maintained in a public repository (if possible) so the process is transparent and can be improved by the community.

7. Search & Linkage Best Practices

Throughout the implementation, keep in mind best practices for reliability and accuracy:

Rate Limiting and API Quotas: When using the YouTube Data API, respect quota limits (e.g., searching and listing videos costs quota points). Use exponential backoff and error handling to avoid crashes if the API quota is exceeded or if there’s a temporary failure. If using scraping as fallback, implement polite crawling delays and possibly rotate user agents/IPs to avoid being blocked.

Accuracy in Matching: The combination of description scanning, pinned comment retrieval, title search, and transcript matching gives a high confidence in linking Shorts to full videos. Many creators explicitly guide viewers from Shorts to longs (e.g., “full video in pinned comment”), so leveraging those cues is critical
reddit.com
. The system should be designed to use the most direct evidence first (explicit links) before attempting fuzzier matches (keyword or transcript search). This minimizes false matches.

Security and Compliance: Only use public data. All the information (video metadata, comments, etc.) is publicly available through YouTube’s interfaces. Ensure the parsing respects YouTube’s terms of service – if using the official API, stick to their rules; if scraping, only gather data that a normal viewer could see (which includes comments, descriptions, etc.). Do not collect personal data beyond what is publicly shown.

Scalability: As the number of channels or videos grows, consider caching results (e.g., store already-scanned video IDs so we don’t fetch the same data every month unnecessarily). Use multithreading or batching when calling APIs to speed up processing, but within safe limits. The monthly interval is generous, so there is plenty of time to scan even large channels by spreading tasks over a few hours if needed.

By following these steps and best practices, the system will be able to continuously parse and update an enterprise-grade mapping of YouTube Shorts to their related long-form videos. The end result is a robust table (as outlined in the prompt) that can be used for analysis, content strategy, or any application requiring insight into how short-form content relates to longer videos on the listed channels. Each monthly update will refine and expand this dataset, ensuring it remains current and comprehensive.
