# -*- coding: utf-8 -*- #
# Copyright 2022 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Get a PipelineRun/TaskRun."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.cloudbuild import cloudbuild_util as v1_client_util
from googlecloudsdk.api_lib.cloudbuild.v2 import client_util as v2_client_util
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.cloudbuild import run_flags
from googlecloudsdk.core import resources


@base.Hidden
@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class Describe(base.Command):
  """Get a PipelineRun/TaskRun/Build."""

  @staticmethod
  def Args(parser):
    """Register flags for this command.

    Args:
      parser: An argparse.ArgumentParser-like object. It is mocked out in order
        to capture some information, but behaves like an ArgumentParser.
    """
    parser = run_flags.AddsRunFlags(parser)

  def Run(self, args):
    """This is what gets called when the user runs this command."""
    region_ref = args.CONCEPTS.region.Parse()
    region = region_ref.AsDict()['locationsId']
    project = region_ref.AsDict()['projectsId']
    run_id = args.RUN_ID

    if args.type == 'build':
      client = v1_client_util.GetClientInstance()
      messages = v1_client_util.GetMessagesModule()
      build_resource = resources.REGISTRY.Parse(
          run_id,
          params={
              'projectsId': project,
              'locationsId': region,
              'buildsId': run_id,
          },
          collection='cloudbuild.projects.locations.builds')
      return client.projects_locations_builds.Get(
          messages.CloudbuildProjectsLocationsBuildsGetRequest(
              name=build_resource.RelativeName()))
    else:
      return v2_client_util.GetRun(project, region, run_id, args.type)
