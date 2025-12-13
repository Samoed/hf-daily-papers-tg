from typing import Literal

from pydantic import BaseModel, Field

RepoType = Literal["dataset", "model", "space"]


class BaseTrendingModel(BaseModel):
    id: str
    likes: int

    @property
    def hf_url(self) -> str:
        return f"https://huggingface.co/{self.id}"

    @property
    def hyperlink(self) -> str:
        return f"<a href='{self.hf_url}'>{self.id}</a>"

    def full_text(self) -> str:
        return f"{self.hyperlink} {self.likes}❤️"


class DatasetTrendingModel(BaseTrendingModel):
    @property
    def hf_url(self) -> str:
        return f"https://huggingface.co/datasets/{self.id}"


class ModelsTrendingModel(BaseTrendingModel):
    pipeline_tag: str | None = None

    def full_text(self) -> str:
        pipeline_tag = " " + self.pipeline_tag if self.pipeline_tag else ""
        return super().full_text() + pipeline_tag


class SpacesTrendingModel(BaseTrendingModel):
    title: str
    ai_short_description: str
    short_description: str | None = Field(None, alias="shortDescription")
    emoji: str

    @property
    def hf_url(self) -> str:
        return f"https://huggingface.co/spaces/{self.id}"

    @property
    def hyperlink(self) -> str:
        return f"<a href='{self.hf_url}'>{self.emoji} {self.title}</a>"

    def full_text(self) -> str:
        description = self.short_description if self.short_description else self.ai_short_description
        return f"{super().full_text()} {description}"


class TrendingModel(BaseModel):
    repo_type: RepoType = Field(alias="repoType")
    repo_data: SpacesTrendingModel | ModelsTrendingModel | DatasetTrendingModel = Field(alias="repoData")


class RecentlyTrendingModel(BaseModel):
    recently_trending: list[TrendingModel] = Field(alias="recentlyTrending")
