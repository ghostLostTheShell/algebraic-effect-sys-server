
from pathlib import Path
from pydantic import BaseModel
import toml


class AppConfig(BaseModel):
  api_prefix: str = "/api/v1"
  log_level: str = "INFO"
  
class LoggingConfig(BaseModel):
    log_to_file: bool = False
    log_file_path: str = "log/app.log"
    log_file_when: str = "D"  # D: daily, H: hourly, M: minutely
    log_file_interval: int = 1
    log_file_backup_count: int = 7
    log_file_encoding: str = "utf-8"
    log_file_level: str = "INFO"
    console_log_level: str = "INFO" 

class RootConfig(BaseModel):
  app: AppConfig = AppConfig()
  logging: LoggingConfig = LoggingConfig()
  
  @property
  def api_prefix(self) -> str:
    return self.app.api_prefix


def load_config(config_path: Path = Path("config.toml")) -> RootConfig:
    if not config_path.exists():
        # 定义默认配置
        default_config_data = RootConfig().model_dump()
        # 将默认配置写入文件

        with open(config_path, mode="w", encoding="utf-8") as fp:
            toml.dump(default_config_data, fp)
        print(f"Created default config file: {config_path}")

    with open(config_path, mode="r", encoding="utf-8") as fp:
        config_data = toml.load(fp)
    return RootConfig(**config_data)

config: RootConfig | None = None

def get_config() -> RootConfig:
  global config
  if config is None:
    config = load_config()
  return config

def get_app_config() -> AppConfig:
  global config
  if config is None:
    config = load_config()
  return config.app


__all__ = ['get_config', 'get_app_config', ]