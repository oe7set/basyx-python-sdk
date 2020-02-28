# Copyright 2019 PyI40AAS Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import unittest

from aas.util.identification import *
from aas import model


class IdentifierGeneratorTest(unittest.TestCase):
    def test_generate_uuid_identifier(self):
        generator = UUIDGenerator()
        identification = generator.generate_id()
        self.assertRegex(identification.id,
                         r"urn:uuid:[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}")
        ids = set()
        for i in range(100):
            identification = generator.generate_id()
            self.assertNotIn(identification, ids)
            ids.add(identification)

    def test_generate_iri_identifier(self):
        provider = model.DictObjectStore()

        # Check expected Errors when Namespaces are not valid
        with self.assertRaises(ValueError) as cm:
            generator = NamespaceIRIGenerator("", provider)
        self.assertEqual('Namespace must be a valid IRI, ending with #, / or =', str(cm.exception))
        with self.assertRaises(ValueError) as cm:
            generator = NamespaceIRIGenerator("http", provider)
        self.assertEqual('Namespace must be a valid IRI, ending with #, / or =', str(cm.exception))

        generator = NamespaceIRIGenerator("http://acplt.org/AAS/", provider)
        self.assertEqual("http://acplt.org/AAS/", generator.namespace)

        identification = generator.generate_id()
        self.assertEqual(identification.id, "http://acplt.org/AAS/0000")
        provider.add(model.Submodel(identification))

        for i in range(10):
            identification = generator.generate_id()
            self.assertNotIn(identification, provider)
            provider.add(model.Submodel(identification))
        self.assertEqual(identification.id, "http://acplt.org/AAS/0010")

        identification = generator.generate_id("Spülmaschine")
        self.assertEqual(identification.id, "http://acplt.org/AAS/Spülmaschine")
        provider.add(model.Submodel(identification))

        for i in range(10):
            identification = generator.generate_id("Spülmaschine")
            self.assertNotIn(identification, provider)
            self.assertNotEqual(identification.id, "http://acplt.org/AAS/Spülmaschine")
