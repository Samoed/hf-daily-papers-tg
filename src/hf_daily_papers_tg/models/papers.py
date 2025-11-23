from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from ._escape import escape


class Paper(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    published_at: str = Field(alias="publishedAt")
    title: str
    summary: str
    upvotes: int = 0
    project_page: HttpUrl | None = Field(None, alias="projectPage")
    github_repo: HttpUrl | None = Field(None, alias="githubRepo")
    github_stars: int | None = Field(None, alias="githubStars")
    ai_summary: str | None = Field(None, alias="ai_summary")
    keywords: list[str] | None = Field(None, alias="ai_keywords")

    @property
    def hf_url(self) -> str:
        return f"https://huggingface.co/papers/{self.id}"


class Organization(BaseModel):
    name: str
    full_name: str = Field(alias="fullname")

    @property
    def hf_url(self) -> str:
        return f"https://huggingface.co/{self.name}"


class PaperModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    paper: Paper
    num_comments: int = Field(alias="numComments")
    organization: Organization | None = None

    def format(self) -> str:
        """Format paper information as HTML for Telegram."""

        org_part = ""
        if self.organization:
            org_part = f" by <a href='{self.organization.hf_url}'>{escape(self.organization.full_name)}</a>"

        title_part = (
            f"<a href='{self.paper.hf_url}'>{escape(self.paper.title)}</a>{org_part} 🔼 {escape(self.paper.upvotes)}"
        )
        ai_summary_part = f"\n\n<b>AI Summary:</b>\n{escape(self.paper.ai_summary)}" if self.paper.ai_summary else ""
        abstract_part = f"\n\n<b>Abstract:</b>\n{escape(self.paper.summary)}"

        gh_repo_part = (
            f"\n\n<a href='{self.paper.github_repo}'>GitHub Repo</a> (⭐ {escape(self.paper.github_stars)})"
            if self.paper.github_repo
            else ""
        )
        project_page_part = (
            f"\n\n<a href='{self.paper.project_page}'>Project Page</a>" if self.paper.project_page else ""
        )

        return title_part + ai_summary_part + abstract_part + gh_repo_part + project_page_part

    @property
    def paper_hyperlink(self) -> str:
        return f"<a href='{self.paper.hf_url}'>{self.paper.title}</a>"
