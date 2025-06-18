import fsspec
import typing
import polars

type FileFormat = typing.Literal['ndjson', 'parquet']

class Storage:
    """
    Wrapper class for reading and writing to storage using Polars dataframes
    """
    
    @classmethod
    def read(cls, source: str, format: FileFormat, credentials: typing.Optional[dict[str, typing.Any]]) -> polars.DataFrame:
        match format:
            case 'ndjson':
                return polars.read_ndjson(source=source, storage_options=credentials)
            case _:
                return polars.read_parquet(source=source, storage_options=credentials)
        
    @classmethod
    def write(cls, destination: str, filesystem: fsspec.spec.AbstractFileSystem, dataframe: polars.DataFrame, format: FileFormat) -> None:
        with filesystem.open(path=destination, mode='wb') as f:
            match format:
                case 'ndjson':
                    dataframe.write_ndjson(f)
                case _:
                    dataframe.write_parquet(f)